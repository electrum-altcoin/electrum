from electrum.bitcoin import base_decode, base_encode, Hash, is_address
from electrum.exceptions import MissingHeader
from electrum.util import inv_dict, read_json, bfh, to_bytes, BitcoinException
from .abstract_network import AbstractNet
from .auxpow_mixin import AuxPowMixin
from .stake_mixin import StakeMixin

class CrowncoinMainnet(AbstractNet, AuxPowMixin, StakeMixin):

    NAME = 'Crown'
    NAME_LOWER = 'crown'
    SHORT_CODE = 'CRW'
    DATA_DIR = 'crown'
    OPEN_ALIAS_PREFIX = 'crw'
    PAYMENT_URI_SCHEME = 'crown'
    PAYMENT_REQUEST_PKI_TYPE = "dnssec+crw"
    APPLICATION_PAYMENT_REQUEST_TYPE = 'application/crown-paymentrequest'
    APPLICATION_PAYMENT_TYPE = 'application/crown-payment'
    APPLICATION_PAYMENT_ACK_TYPE = 'application/crown-paymentack'
    BASE_UNITS = {'CRW': 8, 'mCRW': 5, 'uCRW': 2, 'swartz': 0}
    BASE_UNITS_INVERSE = inv_dict(BASE_UNITS)
    BASE_UNITS_LIST = ['CRW', 'mCRW', 'uCRW', 'swartz']
    TESTNET = False

    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = bfh('017507')
    ADDRTYPE_P2SH = bfh('0174f1')
    XPRV_HEADERS = {
        'standard': 0x0488ade4,
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard': 0x0488b21e,
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 72

    GENESIS = "0000000085370d5e122f64f4ab19c68614ff3df78c8d13cb814fd7e69a1dc6da"

    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers/Crowncoin-Mainnet.json', {})
    CHECKPOINTS = read_json('checkpoints/Crowncoin-Mainnet.json', [])

    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []

    COINBASE_MATURITY = 100
    COIN = 100000000
    TOTAL_COIN_SUPPLY_LIMIT = 21000000
    SIGNED_MESSAGE_PREFIX = b"\x18Crowncoin Signed Message:\n"

    DECIMAL_POINT_DEFAULT = 8 # CRW
    AUXPOW_CHAIN_ID = 0x14
    AUXPOW_START_HEIGHT = 45327
    BLOCK_VERSION_AUXPOW_BIT = 0x100
    DGW_FORK_BLOCK = 1059780
    TARGET_TIMESPAN = int(14 * 24 * 60 * 60)
    TARGET_SPACING = int(60)
    INTERVAL = int(TARGET_TIMESPAN / TARGET_SPACING)

    POS_START_HEIGHT = 2330000
    MIN_POS_WORK_LIMIT = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    BLOCK_EXPLORERS = {
        'CryptoID.info': ('https://chainz.cryptoid.info/crw/', {'tx': 'tx.dws?', 'addr': 'address.dws?'}),
        'system default': ('blockchain:/', {'tx': 'tx/', 'addr': 'address/'}),
    }

    # The default Bitcoin frame size limit of 1 MB doesn't work for AuxPoW-based
    # chains, because those chains' block headers have extra AuxPoW data.
    # we set a limit of 40 MB so that we have extra wiggle room.
    MAX_INCOMING_MSG_SIZE = 40_000_000  # in bytes


    @classmethod
    def get_target(cls, height: int, blockchain) -> int: 
        index = height // 2016 - 1
        if index == -1:
            return cls.MAX_TARGET

        if index < len(blockchain.checkpoints):
            h, t = blockchain.checkpoints[index]
            return t

        if height >= cls.DGW_FORK_BLOCK:
            return cls.get_target_dgw(height, blockchain)
        return cls.get_target_btc(height, blockchain)

    @classmethod
    def get_target_btc(cls, height: int, blockchain) -> int:
        if not height % cls.INTERVAL == 0:
            # Get the first block of this retarget period
            last = blockchain.read_header(height - 1)
            if not last:
                raise MissingHeader()
            return blockchain.bits_to_target(last['bits'])

        # new target
        first = blockchain.read_header(height - cls.INTERVAL)
        last = blockchain.read_header(height - 1)
        if not first or not last:
            raise MissingHeader()

        bits = last.get('bits')
        target = blockchain.bits_to_target(bits)
        nActualTimespan = last.get('timestamp') - first.get('timestamp')
        nActualTimespan = max(nActualTimespan, cls.TARGET_TIMESPAN // 4)
        nActualTimespan = min(nActualTimespan, cls.TARGET_TIMESPAN * 4)
        new_target = min(cls.MAX_TARGET, (target * nActualTimespan) // cls.TARGET_TIMESPAN)
        # not any target can be represented in 32 bits:
        new_target = blockchain.bits_to_target(blockchain.target_to_bits(new_target))
        return new_target

    @classmethod
    def get_target_dgw(cls, height: int, blockchain) -> int:       
        # get last solved header
        current = blockchain.read_header(height - 1)
        nActualTimespan = 0
        lastBlockTime = 0
        pastBlocksMin = 24
        pastBlocksMax = 24
        countBlocks = 0

        for i in range(pastBlocksMax):
            countBlocks += 1
            if not current:
                raise BaseException('header at height: %d is not stored in db' % (height - i - 1))

            bits = current.get('bits')
            if countBlocks <= pastBlocksMin:
                if countBlocks == 1:
                    past_difficulty_avg = blockchain.bits_to_target(bits)
                else:
                    past_difficulty_avg = (past_difficulty_avg_prev * countBlocks + blockchain.bits_to_target(bits)) // (countBlocks + 1)
                past_difficulty_avg_prev = past_difficulty_avg

            if lastBlockTime > 0:
                nActualTimespan += lastBlockTime - current.get('timestamp')
            lastBlockTime = current.get('timestamp')

            # get previous block
            current = blockchain.read_header(height - i - 2)

        target_timespan = countBlocks * cls.TARGET_SPACING
        nActualTimespan = max(nActualTimespan, target_timespan // 3)
        nActualTimespan = min(nActualTimespan, target_timespan * 3)
        new_target = min(cls.MAX_TARGET, (past_difficulty_avg * nActualTimespan) // target_timespan)
        return new_target

    @classmethod
    def hash160_to_b58_address(cls, h160, addrtype) -> str:
        if isinstance(addrtype, bytes):
            s = addrtype
        else:
            s = bfh(addrtype)
        s += h160
        return base_encode(s + Hash(s)[0:4], base=58)

    @classmethod
    def b58_address_to_hash160(cls, addr):
        addr = to_bytes(addr, 'ascii')
        _bytes = base_decode(addr, length=27, base=58)
        return _bytes[0:3], _bytes[3:23]
