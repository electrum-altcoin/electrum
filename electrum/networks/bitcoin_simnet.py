from electrum.util import inv_dict, read_json
from .bitcoin_testnet import BitcoinTestnet

class BitcoinSimnet(BitcoinTestnet):
    NAME = 'Bitcoin Simnet'
    NAME_LOWER = 'simnet bitcoin'
    WIF_PREFIX = 0x64
    ADDRTYPE_P2PKH = 0x3f
    ADDRTYPE_P2SH = 0x7b
    SEGWIT_HRP = "sb"
    GENESIS = "683e86bd5c6d110d91b94b97137ba6bfe02dbbdb8e3dff722a669b5d69d77af6"
    DEFAULT_SERVERS = read_json('servers/Bitcoin-Simnet.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []
    DATA_DIR = 'bitcoin-simnet'