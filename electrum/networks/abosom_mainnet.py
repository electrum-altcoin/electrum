from electrum.util import inv_dict, read_json, bfh
from .abstract_network import AbstractNet
from .stake_mixin import StakeMixin
from ..bitcoin import hash_encode
from ..exceptions import MissingHeader


class AbosomMainnet(AbstractNet, StakeMixin):
    NAME = 'Abosom'
    NAME_LOWER = 'abosom'
    SHORT_CODE = 'ABOSOM'
    DATA_DIR = 'abosom'
    OPEN_ALIAS_PREFIX = 'abosom'
    PAYMENT_URI_SCHEME = 'abosom'
    PAYMENT_REQUEST_PKI_TYPE = "dnssec+abosom"
    APPLICATION_PAYMENT_REQUEST_TYPE = 'application/abosom-paymentrequest'
    APPLICATION_PAYMENT_TYPE = 'application/abosom-payment'
    APPLICATION_PAYMENT_ACK_TYPE = 'application/abosom-paymentack'
    BASE_UNITS = {'ABOSOM': 8, 'mABOSOM': 5, 'uABOSOM': 2, 'satoshi': 0}
    BASE_UNITS_INVERSE = inv_dict(BASE_UNITS)
    BASE_UNITS_LIST = ['ABOSOM', 'mABOSOM', 'uABOSOM', 'satoshi']
    TESTNET = False

    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = 75
    ADDRTYPE_P2SH = 78
    XPRV_HEADERS = {
        'standard': 0x800001c8,
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard': 0x800101c8,
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 704

    GENESIS = "00000e8048ffa0a80549ed405640e95e01590e70baf4888ef594d87402635697"

    DEFAULT_PORTS = {'t': '50041', 's': '50042'}
    DEFAULT_SERVERS = read_json('servers/Abosom-Mainnet.json', {})
    CHECKPOINTS = read_json('checkpoints/Abosom-Mainnet.json', [])

    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []

    COINBASE_MATURITY = 8
    COIN = 1000000
    TOTAL_COIN_SUPPLY_LIMIT = 110000000
    SIGNED_MESSAGE_PREFIX = b"\x18Abosom Signed Message:\n"
    DECIMAL_POINT_DEFAULT = 8 # CRW
    TARGET_TIMESPAN = int(24 * 60 * 60)
    TARGET_SPACING = int(60)
    INTERVAL = int(TARGET_TIMESPAN / TARGET_SPACING)

    POS_START_HEIGHT = 1
    BLOCK_EXPLORERS = {
        'system default': ('blockchain:/', {'tx': 'tx/', 'addr': 'address/'}),
    }

    @classmethod
    def hash_raw_header(cls, header):
        import algomodule
        return hash_encode(algomodule._x11_hash(bfh(header)))

    @classmethod
    def is_pos_active(cls, header) -> bool:
        return True

    @classmethod
    def get_target(cls, height: int, blockchain) -> int:
        index = height // 2016 - 1
        if index == -1:
            return cls.MAX_TARGET

        if index < len(blockchain.checkpoints):
            h, t = blockchain.checkpoints[index]
            return t

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