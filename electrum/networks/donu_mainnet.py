from electrum.bitcoin import base_decode, base_encode, Hash, is_address
from electrum.exceptions import MissingHeader
from electrum.util import inv_dict, read_json, bfh, to_bytes, BitcoinException
from .abstract_network import AbstractNet
from .auxpow_mixin import AuxPowMixin
from .stake_mixin import StakeMixin


class DonuMainnet(AbstractNet, StakeMixin):
    NAME = 'Donu'
    NAME_LOWER = 'donu'
    SHORT_CODE = 'DONU'
    DATA_DIR = 'donu'
    OPEN_ALIAS_PREFIX = 'donu'
    PAYMENT_URI_SCHEME = 'donu'
    PAYMENT_REQUEST_PKI_TYPE = "dnssec+donu"
    APPLICATION_PAYMENT_REQUEST_TYPE = 'application/donu-paymentrequest'
    APPLICATION_PAYMENT_TYPE = 'application/donu-payment'
    APPLICATION_PAYMENT_ACK_TYPE = 'application/donu-paymentack'
    BASE_UNITS = {'DONU': 8, 'mDONU': 5, 'uDONU': 2, 'satoshi': 0}
    BASE_UNITS_INVERSE = inv_dict(BASE_UNITS)
    BASE_UNITS_LIST = ['DONU', 'mDONU', 'uDONU', 'satoshi']
    TESTNET = False

    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = 53
    ADDRTYPE_P2SH = 5
    XPRV_HEADERS = {
        'standard': 0x0488ade4,
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard': 0x0488b21e,
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 405
    SEGWIT_HRP = "dn"

    GENESIS = "000000008507af1fdaaf3fed6173005b23b0febf72e7c2094f11f1d057692182"

    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers/Donu-Mainnet.json', {})
    CHECKPOINTS = read_json('checkpoints/Donu-Mainnet.json', [])

    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []

    COINBASE_MATURITY = 100
    COIN = 1000000
    TOTAL_COIN_SUPPLY_LIMIT = 21000000
    SIGNED_MESSAGE_PREFIX = b"\x18Donu Signed Message:\n"

    DECIMAL_POINT_DEFAULT = 8  # DONU
    TARGET_SPACING = int(2 * 60)

    POS_START_HEIGHT = 0

    BLOCK_EXPLORERS = {
        'CryptoID.info': ('https://chainz.cryptoid.info/donu/', {'tx': 'tx.dws?', 'addr': 'address.dws?'}),
        'system default': ('blockchain:/', {'tx': 'tx/', 'addr': 'address/'}),
    }

    @classmethod
    def get_target(cls, height: int, blockchain) -> int:
        index = height // 2016 - 1
        if index == -1:
            return cls.MAX_TARGET

        # Blockchain is PURE POS so we dont have the info needed to
        # calculate the targets required
        return 0

