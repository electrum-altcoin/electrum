from electrum.util import inv_dict, read_json
from .bitcoin_testnet import BitcoinTestnet

class BitcoinRegtest(BitcoinTestnet):
    NAME = 'Bitcoin Regtest'
    NAME_LOWER = 'regtest bitcoin'
    SEGWIT_HRP = "bcrt"
    GENESIS = "0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206"
    DEFAULT_SERVERS = read_json('servers/Bitcoin-Regtest.json', {})
    LN_DNS_SEEDS = []
    DATA_DIR = 'bitcoin-regtest'
