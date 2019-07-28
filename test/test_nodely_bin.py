import os
import platform
import re
from subprocess import PIPE, STDOUT

import pytest
from path import Path

import nodely.bin
from nodely import NodeCommandError
from nodely.bin import Command


WIN = platform.system() == 'Windows'


def test_NODE_MODULES_DIR():
    assert nodely.bin.NODE_MODULES_DIR is nodely.NODE_MODULES_DIR


@pytest.mark.usefixtures('install_node_package')
class TestModule(object):

    def test__name__(self):
        assert nodely.bin.__name__ == nodely.bin.ORIGIN.__name__

    def test__doc__(self):
        assert nodely.bin.__doc__ == nodely.bin.ORIGIN.__doc__

    def test__getitem__(self, node_package_command):
        command = nodely.bin[node_package_command]
        assert type(command) is Command
        assert Path(command).normcase() \
            == nodely.which(node_package_command).normcase()

    def test__getitem__non_existent(self):
        with pytest.raises((IOError, OSError)):
            nodely.bin['non-existent']

    def test__getattr__(self, node_package_command):
        command = getattr(nodely.bin, node_package_command)
        assert type(command) is Command
        assert Path(command).normcase() \
            == nodely.which(node_package_command).normcase()

    def test__getattr__non_existent(self):
        with pytest.raises((IOError, OSError)):
            getattr(nodely.bin, 'non_existent')

    def test__getattr__non_existent__special__(self):
        with pytest.raises(AttributeError) as exc:
            getattr(nodely.bin, '__non_existent__')
        exc.match(
            r"^{!r} has no attribute '__non_existent__'$"
            .format(nodely.bin).replace('\\', r'\\'))

    def test__dir__(self):
        cmdnames = (f.basename()
                    for f in (nodely.bin.NODE_MODULES_DIR / '.bin').files())
        if WIN:
            cmdnames = (cmd for cmd in cmdnames if cmd.ext.lower() != '.cmd')
        assert set(cmdnames).issubset(dir(nodely.bin))


@pytest.mark.usefixtures('install_node_package')
class TestCommand(object):

    def test__new__(self, node_package_command):
        command = Command(node_package_command)
        assert Path(command).normcase() \
            == nodely.which(node_package_command).normcase()

    def test__new__non_existent(self):
        with pytest.raises((IOError, OSError)):
            Command('non_existent')

    def test_name(self, node_package_command):
        assert Command.name is not Path.name
        assert Command(node_package_command).name == node_package_command

    def test_Popen(
            self, node_package_command, node_package_command_args,
            node_package_command_output_regex):
        command = Command(node_package_command)
        process = command.Popen(
            node_package_command_args, stdout=PIPE, stderr=PIPE,
            universal_newlines=True)

        out, err = process.communicate()
        assert process.returncode is 0
        assert node_package_command_output_regex.match(out.strip())
        assert not err

    def test_Popen_non_zero_returncode(self, node_package_command):
        command = Command(node_package_command)
        process = command.Popen(
            '--non-existent', stdout=PIPE, stderr=PIPE,
            universal_newlines=True)

        out, err = process.communicate()
        assert process.returncode is not 0
        assert not out and err

    def test_call(
            self, capfd, node_package_command, node_package_command_args,
            node_package_command_output_regex):
        command = Command(node_package_command)
        assert command.call(node_package_command_args) is 0

        out, err = capfd.readouterr()
        assert node_package_command_output_regex.match(out.strip())
        assert not err

    def test_call_non_zero_returncode(self, capfd, node_package_command,):
        command = Command(node_package_command)
        assert command.call(['--non-existent']) is not 0

        out, err = capfd.readouterr()
        assert not out and err

    def test_check_call_raises(self, capfd, node_package_command):
        command = Command(node_package_command)
        with pytest.raises(NodeCommandError, match=(
                r"^Command '\[[^,]+, '--non-existent'\]' "
                r"returned non-zero exit status -?\d+ "
                r"in working directory {}$"
                .format(re.escape(repr(os.getcwd()))))):

            command.check_call(['--non-existent'])

        out, err = capfd.readouterr()
        assert not out and err

    def test_check_output(
            self, capfd, node_package_command, node_package_command_args,
            node_package_command_output_regex):
        command = Command(node_package_command)
        assert node_package_command_output_regex.match(
            command.check_output(
                node_package_command_args, universal_newlines=True))

        out, err = capfd.readouterr()
        assert not out and not err

    def test_check_output_raises(self, capfd, node_package_command):
        command = Command(node_package_command)
        with pytest.raises(NodeCommandError, match=(
                r"^Command '\[[^,]+, '--non-existent'\]' "
                r"returned non-zero exit status -?\d+ "
                r"in working directory {}$"
                .format(re.escape(repr(os.getcwd()))))):

            command.check_output(['--non-existent'], stderr=STDOUT)

        out, err = capfd.readouterr()
        assert not out and not err

    def test__call__(
            self, capfd, node_package_command, node_package_command_args,
            node_package_command_output_regex):
        command = Command(node_package_command)
        assert node_package_command_output_regex.match(
            command(*node_package_command_args, universal_newlines=True))

        out, err = capfd.readouterr()
        assert not out and not err

    def test__call__raises(self, capfd, node_package_command):
        command = Command(node_package_command)
        with pytest.raises(NodeCommandError, match=(
                r"^Command '\[[^,]+, '--non-existent', '--and-invalid'\]' "
                r"returned non-zero exit status -?\d+ "
                r"in working directory {}$"
                .format(re.escape(repr(os.getcwd()))))):

            command('--non-existent', '--and-invalid', stderr=STDOUT)

        out, err = capfd.readouterr()
        assert not out and not err

    def test__repr__(self, node_package_command):
        assert (
            repr(Command(node_package_command)) ==
            "nodely.bin['{}']".format(node_package_command))
