from electrum.util import inv_dict, read_json
from .bitcoin_mainnet import BitcoinMainnet

class BitcoinTestnet(BitcoinMainnet):

    NAME = 'Bitcoin Testnet'
    NAME_LOWER = 'testnet bitcoin'
    TESTNET = True
    WIF_PREFIX = 0xef
    ADDRTYPE_P2PKH = 111
    ADDRTYPE_P2SH = 196
    SEGWIT_HRP = "tb"
    GENESIS = "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers/Bitcoin-Testnet.json', {})
    CHECKPOINTS = read_json('checkpoints/Bitcoin-Testnet.json', [])
    DATA_DIR = 'bitcoin-testnet'
    BASE_UNITS = {'BTC': 8, 'mBTC': 5, 'bits': 2, 'sat': 0}
    BASE_UNITS_INVERSE = inv_dict(BASE_UNITS)
    BASE_UNITS_LIST = ['BTC', 'mBTC', 'bits', 'sat']
    
    XPRV_HEADERS = {
        'standard':    0x04358394,  # tprv
        'p2wpkh-p2sh': 0x044a4e28,  # uprv
        'p2wsh-p2sh':  0x024285b5,  # Uprv
        'p2wpkh':      0x045f18bc,  # vprv
        'p2wsh':       0x02575048,  # Vprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x043587cf,  # tpub
        'p2wpkh-p2sh': 0x044a5262,  # upub
        'p2wsh-p2sh':  0x024289ef,  # Upub
        'p2wpkh':      0x045f1cf6,  # vpub
        'p2wsh':       0x02575483,  # Vpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 1
    LN_DNS_SEEDS = [  # TODO investigate this again
        # 'test.nodes.lightning.directory.',  # times out.
        # 'lseed.bitcoinstats.com.',  # ignores REALM byte and returns mainnet peers...
    ]
    BLOCK_EXPLORERS = {
        'Bitaps.com': ('https://tbtc.bitaps.com/', {'tx': '', 'addr': ''}),
        'BlockCypher.com': ('https://live.blockcypher.com/btc-testnet/', {'tx': 'tx/', 'addr': 'address/'}),
        'Blockchain.info': ('https://www.blockchain.com/btctest/', {'tx': 'tx/', 'addr': 'address/'}),
        'Blockstream.info': ('https://blockstream.info/testnet/', {'tx': 'tx/', 'addr': 'address/'}),
        'smartbit.com.au': ('https://testnet.smartbit.com.au/', {'tx': 'tx/', 'addr': 'address/'}),
        'system default': ('blockchain://000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943/', {'tx': 'tx/', 'addr': 'address/'}),
    }