from electrum.exceptions import MissingHeader
from electrum.util import inv_dict, read_json
from .abstract_network import AbstractNet
from .auxpow_mixin import AuxPowMixin


class NamecoinMainnet(AbstractNet, AuxPowMixin):

    NAME = 'Namecoin'
    NAME_LOWER = 'namecoin'
    SHORT_CODE = 'NMC'
    TESTNET = False
    WIF_PREFIX = 180
    ADDRTYPE_P2PKH = 52
    ADDRTYPE_P2SH = 13
    SEGWIT_HRP = "nc"
    GENESIS = "000000000062b72c5e2ceb45fbc8587e807c155b0da735e6483dfba2f0a9c770"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers/Namecoin-Mainnet.json', {})
    CHECKPOINTS = read_json('checkpoints/Namecoin-Mainnet.json', [])
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 497000
    DATA_DIR = 'namecoin'

    XPRV_HEADERS = {
        'standard':    0x0488ade4,  # xprv
        'p2wpkh-p2sh': 0x049d7878,  # yprv
        'p2wsh-p2sh':  0x0295b005,  # Yprv
        'p2wpkh':      0x04b2430c,  # zprv
        'p2wsh':       0x02aa7a99,  # Zprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x0488b21e,  # xpub
        'p2wpkh-p2sh': 0x049d7cb2,  # ypub
        'p2wsh-p2sh':  0x0295b43f,  # Ypub
        'p2wpkh':      0x04b24746,  # zpub
        'p2wsh':       0x02aa7ed3,  # Zpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 7
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []
    PAYMENT_URI_PREFIX = 'namecoin:'
    APPLICATION_PAYMENT_REQUEST_TYPE = 'application/namecoin-paymentrequest'
    APPLICATION_PAYMENT_TYPE = 'application/namecoin-payment'
    APPLICATION_PAYMENT_ACK_TYPE = 'application/namecoin-paymentack'
    COINBASE_MATURITY = 100
    COIN = 100000000
    TOTAL_COIN_SUPPLY_LIMIT = 21000000
    SIGNED_MESSAGE_PREFIX = b"\x18Namecoin Signed Message:\n"
    TARGET_TIMESPAN = 1209600 # 14 * 24 * 60 * 60
    TARGET_SPACING = 600
    INTERVAL = 2016
    
    BASE_UNITS = {'NMC': 8, 'mNMC': 5, 'uNMC': 2, 'swartz': 0}
    BASE_UNITS_INVERSE = inv_dict(BASE_UNITS)
    BASE_UNITS_LIST = ['NMC', 'mNMC', 'uNMC', 'swartz']
    DECIMAL_POINT_DEFAULT = 5  # mNMC
    AUXPOW_CHAIN_ID = 0x0001
    AUXPOW_START_HEIGHT = 19200
    BLOCK_VERSION_AUXPOW_BIT = 0x100

    BLOCK_EXPLORERS = {
        'Cyphrs.com': ('https://namecoin.cyphrs.com/', {'tx': 'tx/', 'addr': 'address/'}),
        'Namecha.in (non-libre; wiretapped by Cloudflare; discriminates against Tor)': ('https://namecha.in/', {'tx': 'tx/', 'addr': 'address/'}),
        'Bchain.info (non-libre; no name support)': ('https://bchain.info/NMC/', {'tx': 'tx/', 'addr': 'addr/'}),
        'BitInfoCharts.com (non-libre; wiretapped by Cloudflare; discriminates against Tor; no name support)': ('https://bitinfocharts.com/namecoin/', {'tx': 'tx/', 'addr': 'address/'}),
        'mynode.local': ('http://mynode.local:3002/', {'tx': 'tx/', 'addr': 'address/'}),
        'system default': ('blockchain:/', {'tx': 'tx/', 'addr': 'address/'}),
    }

    # The default Bitcoin frame size limit of 1 MB doesn't work for AuxPoW-based
    # chains, because those chains' block headers have extra AuxPoW data.  A limit
    # of 10 MB works fine for Namecoin as of block height 418744 (5 MB fails after
    # height 155232); we set a limit of 20 MB so that we have extra wiggle room.
    MAX_INCOMING_MSG_SIZE = 20_000_000  # in bytes
    
    @classmethod
    def get_target(cls, index: int, blockchain) -> int:
        if index == -1:
            return cls.MAX_TARGET
        if index < len(blockchain.checkpoints):
            h, t = blockchain.checkpoints[index]
            return t

        # new target
        if (index * 2016 + 2015 > 19200) and (index * 2016 + 2015 + 1 > 2016):
            # Namecoin: Apply retargeting hardfork after AuxPoW start
            first = blockchain.read_header(index * 2016 - 1)
        else:
            first = blockchain.read_header(index * 2016)
        last = blockchain.read_header(index * 2016 + 2015)
        if not first or not last:
            raise MissingHeader()

        bits = last.get('bits')
        target = blockchain.bits_to_target(bits)
        nActualTimespan = last.get('timestamp') - first.get('timestamp')
        nTargetTimespan = 14 * 24 * 60 * 60
        nActualTimespan = max(nActualTimespan, nTargetTimespan // 4)
        nActualTimespan = min(nActualTimespan, nTargetTimespan * 4)
        new_target = min(cls.MAX_TARGET, (target * nActualTimespan) // nTargetTimespan)
        # not any target can be represented in 32 bits:
        new_target = blockchain.bits_to_target(blockchain.target_to_bits(new_target))
        return new_target