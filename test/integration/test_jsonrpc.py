import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from aitherd import AitherDaemon
from aither_config import AitherConfig


def test_aitherd():
    config_text = AitherConfig.slurp_config_file(config.aither_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000033b01055cf8df90b01a14734cae92f7039b9b0e48887b4e33a469d7bc07'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000c958ba1a0fe2174effe57a7f39c4c32b8341f1efa20be78b48b6b6bb353'

    creds = AitherConfig.get_rpc_creds(config_text, network)
    aitherd = AitherDaemon(**creds)
    assert aitherd.rpc_command is not None

    assert hasattr(aitherd, 'rpc_connection')

    # Aither testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = aitherd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert aitherd.rpc_command('getblockhash', 0) == genesis_hash
