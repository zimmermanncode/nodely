import re

import pytest
from path import Path

import nodely


TEST_DIR = (
    Path(__file__)  # pylint: disable=no-value-for-parameter
    .realpath().dirname())

exec((TEST_DIR / 'variables.py').text())


@pytest.fixture
def node_package():
    return NODE_PACKAGE  # pylint: disable=undefined-variable


@pytest.fixture
def install_node_package(node_package):
    nodely.install(node_package)


@pytest.fixture
def node_package_command():
    return 'coffee'


@pytest.fixture
def node_package_command_args():
    return ['--version']


@pytest.fixture
def node_package_command_output_regex():
    return re.compile(r"^CoffeeScript version [0-9.]+$")
