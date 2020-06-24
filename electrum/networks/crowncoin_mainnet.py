from electrum.bitcoin import base_decode, base_encode, Hash, is_address
from electrum.exceptions import MissingHeader
from electrum.util import inv_dict, read_json, bfh, to_bytes, BitcoinException
from .abstract_network import AbstractNet
from .auxpow_mixin import AuxPowMixin


class CrowncoinMainnet(AbstractNet, AuxPowMixin):

    NAME = 'Crowncoin'
    NAME_LOWER = 'crowncoin'
    SHORT_CODE = 'CRW'
    TESTNET = False
    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = bfh('017507')
    ADDRTYPE_P2SH = bfh('0174f1')
    GENESIS = "0000000085370d5e122f64f4ab19c68614ff3df78c8d13cb814fd7e69a1dc6da"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers/Crowncoin-Mainnet.json', {})
    CHECKPOINTS = read_json('checkpoints/Crowncoin-Mainnet.json', [])
    DATA_DIR = 'crowncoin'

    XPRV_HEADERS = {
        'standard': 0x0488ade4,
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard': 0x0488b21e,
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 72
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []
    PAYMENT_URI_PREFIX = 'crowncoin:'
    APPLICATION_PAYMENT_REQUEST_TYPE = 'application/crowncoin-paymentrequest'
    APPLICATION_PAYMENT_TYPE = 'application/crowncoin-payment'
    APPLICATION_PAYMENT_ACK_TYPE = 'application/crowncoin-paymentack'
    COINBASE_MATURITY = 100
    COIN = 100000000
    TOTAL_COIN_SUPPLY_LIMIT = 21000000
    SIGNED_MESSAGE_PREFIX = b"\x18Crowncoin Signed Message:\n"

    BASE_UNITS = {'CRW': 8, 'mCRW': 5, 'uCRW': 2, 'swartz': 0}
    BASE_UNITS_INVERSE = inv_dict(BASE_UNITS)
    BASE_UNITS_LIST = ['CRW', 'mCRW', 'uCRW', 'swartz']
    DECIMAL_POINT_DEFAULT = 8  # CRW
    AUXPOW_CHAIN_ID = 0x14
    AUXPOW_START_HEIGHT = 45327
    BLOCK_VERSION_AUXPOW_BIT = 0x100
    DGW_FORK_BLOCK = 1059780
    POS_FORK_BLOCK = 2330000
    TARGET_TIMESPAN = 1209600 # 14 * 24 * 60 * 60
    TARGET_SPACING = 60
    INTERVAL = 20160

    BLOCK_EXPLORERS = {
        'CryptoID.info': ('https://chainz.cryptoid.info/crw/', {'tx': 'tx.dws?', 'addr': 'address.dws?'}),
        'system default': ('blockchain:/', {'tx': 'tx/', 'addr': 'address/'}),
    }

    # The default Bitcoin frame size limit of 1 MB doesn't work for AuxPoW-based
    # chains, because those chains' block headers have extra AuxPoW data.
    # we set a limit of 20 MB so that we have extra wiggle room.
    MAX_INCOMING_MSG_SIZE = 20_000_000  # in bytes
    

    @classmethod
    def get_target(cls, index: int, blockchain) -> int:        
        height = index * 2016 + 2016 - 1

        DIFF_DGW = 0
        DIFF_BTC = 1

        if index == -1:
            return cls.MAX_TARGET
            
        if index < len(blockchain.checkpoints):
            h, t = blockchain.checkpoints[index]
            return t

        retarget = DIFF_DGW
        if height >= cls.DGW_FORK_BLOCK:
            retarget = DIFF_DGW
        else:
            retarget = DIFF_BTC

        if height >= cls.POS_FORK_BLOCK - 1:
            return cls.MAX_TARGET

        if retarget == DIFF_BTC:
            return cls.get_target_btc(index, height, blockchain)
        return cls.get_target_dgw(index, height, blockchain)

    @classmethod
    def get_target_btc(cls, index: int, height: int, blockchain) -> int:
        print(f"[Crown](GetTargetBTC) Height: {height}, Blockchain Height: {blockchain.height()}")

        # new target
        first = blockchain.read_header(index * 2016)
        last = blockchain.read_header(index * 2016 + 2016 - 1)
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
    def get_target_dgw(cls, index: int, height: int, blockchain) -> int:
        print(f"[Crown](GetTargetDGW) Height: {height}, Blockchain Height: {blockchain.height()}")
        # get last solved header
        current = blockchain.read_header(height - 1)
        actual_timespan = 0
        last_block_time = 0
        past_blocks_min = past_blocks_max = 24
        blocks_count = 0
        
        for i in range(past_blocks_max):
            blocks_count += 1
            if not current:
                raise BaseException('header at height: %d is not stored in db' % (height - i - 1))
            bits = current.get('bits')
            if blocks_count <= past_blocks_min:
                if blocks_count == 1:
                    past_difficulty_avg = blockchain.bits_to_target(bits)
                else:
                    past_difficulty_avg = (past_difficulty_avg_prev * blocks_count + blockchain.bits_to_target(bits)) // (blocks_count + 1)
                past_difficulty_avg_prev = past_difficulty_avg

            if last_block_time > 0:
                actual_timespan += last_block_time - current.get('timestamp')
            last_block_time = current.get('timestamp')

            # get previous block
            current = blockchain.read_header(height - i - 2)

        target_timespan = blocks_count * cls.TARGET_SPACING
        actual_timespan = max(actual_timespan, target_timespan // 3)
        actual_timespan = min(actual_timespan, target_timespan * 3)
        new_target = min(cls.MAX_TARGET, (past_difficulty_avg * actual_timespan) // target_timespan)
        return new_target

    @classmethod
    def hash160_to_b58_address(cls, h160: bytes, addrtype: int) -> str:
        s = addrtype + h160
        return base_encode(s+Hash(s)[0:4], base=58)

    @classmethod
    def b58_address_to_hash160(cls, addr):
        addr = to_bytes(addr, 'ascii')
        _bytes = base_decode(addr, length=27, base=58)
        return _bytes[0:3], _bytes[3:23]