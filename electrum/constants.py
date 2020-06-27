# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .networks import *

GIT_REPO_URL = "https://github.com/spesmilo/electrum"
GIT_REPO_ISSUES_URL = "https://github.com/spesmilo/electrum/issues"

networks = {
    'Bitcoin': BitcoinMainnet,
    'Bitcoin-Mainnet': BitcoinMainnet,
    'Bitcoin-Testnet': BitcoinTestnet,
    'Bitcoin-Regtest': BitcoinRegtest,
    'Bitcoin-Simnet': BitcoinSimnet,
    'Crowncoin': CrowncoinMainnet,
    'Crowncoin-Mainnet': CrowncoinMainnet,
    'Namecoin': NamecoinMainnet,
    'Namecoin-Mainnet': NamecoinMainnet,
}

net = networks['Bitcoin']

def select_network(network='Bitcoin'):
    if not network in networks:
        raise Exception('Invalid Network. Available: {}'.format(
            list(networks.keys())))
    global net
    net = networks.get(network, 'Bitcoin')
    return