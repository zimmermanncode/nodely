from subprocess import PIPE
import platform
import re
import sys

from path import Path
import pytest

import nodely


WIN = platform.system() == 'Windows'


def test_NODE_MODULES_DIR():
    assert nodely.NODE_MODULES_DIR == Path(sys.prefix) / 'node_modules'
    assert nodely.NODE_MODULES_DIR.isdir()


def test_install(node_package):
    node_package_dir = nodely.NODE_MODULES_DIR / node_package
    nodely.install(node_package)
    assert node_package_dir.isdir()
    nodely.uninstall(node_package)
    assert not node_package_dir.exists()
    nodely.install(node_package)
    assert node_package_dir.isdir()


def test_install_non_existent():
    with pytest.raises(RuntimeError):
        nodely.install('non-existent')


def test_which(node_package, node_package_command):
    nodely.install(node_package)
    path = Path(nodely.NODE_MODULES_DIR / '.bin' / node_package_command)
    if WIN:
        path += '.cmd'
    assert nodely.which(node_package_command).normcase() == path.normcase()
    assert nodely.which('non-existent') is None


def test_Popen(node_package_command, node_package_command_args,
               node_package_command_output_regex):
    process = nodely.Popen(node_package_command, node_package_command_args,
                           stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out, err = process.communicate()
    assert node_package_command_output_regex.match(out.strip())
    assert not err


def test_call(capfd, node_package_command, node_package_command_args,
              node_package_command_output_regex):
    assert nodely.call(node_package_command, node_package_command_args) is 0
    out, err = capfd.readouterr()
    assert node_package_command_output_regex.match(out.strip())
    assert not err
