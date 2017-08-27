import re

import pytest

import nodely


@pytest.fixture
def node_package():
    return 'coffee-script'


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
