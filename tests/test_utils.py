import os,sys
sys.path.append(os.path.dirname(os.getcwd()))

from src import utils

def test_log():
    assert(utils.log('test' is None))

def test_always_passes():
    assert True

def test_always_fails():
    assert False