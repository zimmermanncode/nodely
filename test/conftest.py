import re

import pytest

import nodely


NODE_PACKAGE = 'coffee-script'


@pytest.fixture
def node_package():
    return NODE_PACKAGE


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
