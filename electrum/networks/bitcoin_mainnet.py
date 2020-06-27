from electrum.exceptions import MissingHeader
from electrum.util import inv_dict, read_json
from .abstract_network import AbstractNet

class BitcoinMainnet(AbstractNet):

    NAME = 'Bitcoin'
    NAME_LOWER = 'bitcoin'
    SHORT_CODE = 'BTC'
    TESTNET = False
    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = 0
    ADDRTYPE_P2SH = 5
    SEGWIT_HRP = "bc"
    GENESIS = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers/Bitcoin-Mainnet.json', {})
    CHECKPOINTS = read_json('checkpoints/Bitcoin-Mainnet.json', [])
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 497000
    DATA_DIR = None

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

    BIP44_COIN_TYPE = 0
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = [
        'nodes.lightning.directory.',
        'lseed.bitcoinstats.com.',
    ]

    APPLICATION_PAYMENT_REQUEST_TYPE = 'application/bitcoin-paymentrequest'
    APPLICATION_PAYMENT_TYPE = 'application/bitcoin-payment'
    APPLICATION_PAYMENT_ACK_TYPE = 'application/bitcoin-paymentack'
    OPEN_ALIAS_PREFIX = 'btc'
    PAYMENT_URI_SCHEME = 'bitcoin'
    PAYMENT_REQUEST_PKI_TYPE = "dnssec+btc"
    COINBASE_MATURITY = 100
    COIN = 100000000
    TOTAL_COIN_SUPPLY_LIMIT = 21000000
    SIGNED_MESSAGE_PREFIX = b"\x18Bitcoin Signed Message:\n"

    BASE_UNITS = {'BTC': 8, 'mBTC': 5, 'bits': 2, 'sat': 0}
    BASE_UNITS_INVERSE = inv_dict(BASE_UNITS)
    BASE_UNITS_LIST = ['BTC', 'mBTC', 'bits', 'sat']
    DECIMAL_POINT_DEFAULT = 5  # mBTC
    BLOCK_EXPLORERS = {
        'Bitupper Explorer': ('https://bitupper.com/en/explorer/bitcoin/',
                              {'tx': 'transactions/', 'addr': 'addresses/'}),
        'Bitflyer.jp': ('https://chainflyer.bitflyer.jp/',
                        {'tx': 'Transaction/', 'addr': 'Address/'}),
        'Blockchain.info': ('https://blockchain.com/btc/',
                            {'tx': 'tx/', 'addr': 'address/'}),
        'blockchainbdgpzk.onion': ('https://blockchainbdgpzk.onion/',
                                   {'tx': 'tx/', 'addr': 'address/'}),
        'Blockstream.info': ('https://blockstream.info/',
                             {'tx': 'tx/', 'addr': 'address/'}),
        'Bitaps.com': ('https://btc.bitaps.com/',
                       {'tx': '', 'addr': ''}),
        'BTC.com': ('https://btc.com/',
                    {'tx': '', 'addr': ''}),
        'Chain.so': ('https://www.chain.so/',
                     {'tx': 'tx/BTC/', 'addr': 'address/BTC/'}),
        'Insight.is': ('https://insight.bitpay.com/',
                       {'tx': 'tx/', 'addr': 'address/'}),
        'TradeBlock.com': ('https://tradeblock.com/blockchain/',
                           {'tx': 'tx/', 'addr': 'address/'}),
        'BlockCypher.com': ('https://live.blockcypher.com/btc/',
                            {'tx': 'tx/', 'addr': 'address/'}),
        'Blockchair.com': ('https://blockchair.com/bitcoin/',
                           {'tx': 'transaction/', 'addr': 'address/'}),
        'blockonomics.co': ('https://www.blockonomics.co/',
                            {'tx': 'api/tx?txid=', 'addr': '#/search?q='}),
        'OXT.me': ('https://oxt.me/',
                   {'tx': 'transaction/', 'addr': 'address/'}),
        'smartbit.com.au': ('https://www.smartbit.com.au/',
                            {'tx': 'tx/', 'addr': 'address/'}),
        'mynode.local': ('http://mynode.local:3002/',
                         {'tx': 'tx/', 'addr': 'address/'}),
        'system default': ('blockchain:/',
                           {'tx': 'tx/', 'addr': 'address/'}),
    }

    TARGET_TIMESPAN = int(14 * 24 * 60 * 60)
    TARGET_SPACING = int(10 * 60)
    INTERVAL = int(TARGET_TIMESPAN / TARGET_SPACING)

    @classmethod
    def get_target(cls, height: int, blockchain) -> int:
        index = height // 2016 - 1

        if index == -1:
            return cls.MAX_TARGET

        if index < len(blockchain.checkpoints):
            h, t = blockchain.checkpoints[index]
            return t

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
