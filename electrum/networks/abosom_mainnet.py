from electrum.util import inv_dict, read_json
from .abstract_network import AbstractNet
from .stake_mixin import StakeMixin


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
        'standard': 0x800001c8,
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
    POS_START_HEIGHT = 1
    BLOCK_EXPLORERS = {
        'system default': ('blockchain:/', {'tx': 'tx/', 'addr': 'address/'}),
    }