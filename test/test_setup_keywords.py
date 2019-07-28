import os
import sys

import pytest
import zetup

from nodely.setup_keywords import require_node_modules
import nodely


def test_require_node_modules(node_package):
    node_package_dir = nodely.NODE_MODULES_DIR / node_package
    nodely.uninstall(node_package)
    assert not node_package_dir.exists()
    require_node_modules(dist=None, jsmodules=[node_package])
    assert node_package_dir.isdir()


def test_require_node_modules_from_string(node_package):
    node_package_dir = nodely.NODE_MODULES_DIR / node_package
    nodely.uninstall(node_package)
    assert not node_package_dir.exists()
    require_node_modules(dist=None, jsmodules="""
    {}
    """.format(node_package))
    assert node_package_dir.isdir()


def test_require_node_modules_with_wrong_keyword():
    with pytest.raises(AssertionError):
        require_node_modules(dist=None, keyword='wrong')


def test_require_node_modules_without_jsmodules(node_package):
    nodely.uninstall(node_package)
    node_modules_content = nodely.NODE_MODULES_DIR.listdir()
    require_node_modules(dist=None)
    assert node_modules_content == nodely.NODE_MODULES_DIR.listdir()


# def test_setup(node_package):
#     node_package_dir = nodely.NODE_MODULES_DIR / node_package
#     nodely.uninstall(node_package)
#     assert not node_package_dir.exists()
#     zetup.call(
#         [sys.executable, 'setup.py', 'develop'],
#         cwd=os.path.dirname(os.path.realpath(__file__)))
#     assert node_package_dir.isdir()
