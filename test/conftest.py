import re

import pytest


@pytest.fixture
def node_package():
    return 'coffee-script'


@pytest.fixture
def node_package_command():
    return 'coffee'


@pytest.fixture
def node_package_command_args():
    return ['--version']


@pytest.fixture
def node_package_command_output_regex():
    return re.compile(r"^CoffeeScript version [0-9.]+$")
