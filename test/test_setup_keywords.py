import os
import sys

import pytest
import zetup

import nodely


def test_setup_entry_point(node_package):
    node_package_dir = nodely.NODE_MODULES_DIR / node_package
    nodely.uninstall(node_package)
    assert not node_package_dir.exists()
    nodely.setup_entry_point(dist=None, jsmodules=[node_package])
    assert node_package_dir.isdir()


def test_setup_entry_point_with_wrong_keyword():
    with pytest.raises(AssertionError):
        nodely.setup_entry_point(dist=None, keyword='wrong')


def test_require_node_modules(node_package):
    node_package_dir = nodely.NODE_MODULES_DIR / node_package
    nodely.uninstall(node_package)
    assert not node_package_dir.exists()
    zetup.call([sys.executable, 'setup.py', 'develop'],
               cwd=os.path.dirname(os.path.realpath(__file__)))
    assert node_package_dir.isdir()
