# nodely >>> putMORE Node.js into Python
#
# Copyright (C) 2017 Stefan Zimmermann <user@zimmermann.co>
#
# nodely is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nodely is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with nodely.  If not, see <http://www.gnu.org/licenses/>.

"""
nodely.bin

Command proxy to the ``node_modules/.bin/`` directory
"""

from subprocess import CalledProcessError, PIPE
from types import ModuleType
import os
import platform
import sys

from path import Path
import zetup

from nodely import NODE_MODULES_DIR

from .error import NodeCommandError

__all__ = ['Command']


#: Running on Windows?
WIN = platform.system() == 'Windows'


#: The original nodely.bin module object
ORIGIN = sys.modules[__name__]


class Module(ModuleType):
    """
    Wrapper module class for :mod:`nodely.bin`.

    Makes module directly act as command proxy to the ``node_modules/.bin/``
    directory via :meth:`.__getitem__` and :meth:`.__getattr__`
    """

    def __init__(self):
        """
        Set ``.__name__`` and ``.__doc__``, and update ``.__dict__``.

        All taken from original ``nodely.bin`` module
        """
        super(Module, self).__init__(__name__, ORIGIN.__doc__)
        self.__dict__.update(ORIGIN.__dict__)

    def __getitem__(self, cmdname):
        """
        Get a :class:`nodely.bin.Command` instance for given `cmdname`.

        :raises OSError: if executable can not be found
        """
        return Command(cmdname)

    def __getattr__(self, name):
        """
        Get a :class:`nodely.bin.Command` instance for given command `name`.

        :raises OSError: if executable cannot be found
        """
        try:  # first check if original module has the given attribute
            return getattr(ORIGIN, name)
        except AttributeError:
            pass
        # and don't treat special Python member names as Node.js commands
        if name.startswith('__'):
            raise AttributeError(
                "{!r} has no attribute {!r}".format(self, name))
        return self[name]

    def __dir__(self):
        cmdnames = (f.basename()
                    for f in (NODE_MODULES_DIR / '.bin').files())
        if WIN:  # pragma: no cover
            cmdnames = (cmd for cmd in cmdnames if cmd.ext.lower() != '.cmd')
        return dir(ORIGIN) + list(cmdnames)


# replace nodely.bin module with wrapper instance
sys.modules[__name__] = Module()


class Command(zetup.object, Path):
    """
    A Node.js executable from current Python environment.

    Residing in ``node_modules/.bin/``
    """

    def __new__(cls, name):
        """
        Check existance and store absolute path in ``path.Path`` base.

        :param name:
            The basename of the executable in ``node_modules/.bin``
        :raises OSError:
            if executable cannot be found
        """
        if WIN:  # pragma: no cover
            name += '.cmd'
        cmd = Path.__new__(cls, NODE_MODULES_DIR / '.bin' / name)
        cmd.atime  # HACK: raises OSError if not existing
        return cmd

    def __init__(self, name):
        """:meth:`.__new__` does all the work :)."""
        pass

    @property
    def name(self):
        """Get the name of this Node.js command."""
        name = Path(self).basename()
        if WIN:  # pragma: no cover
            # remove .cmd file extension
            name = name.splitext(  # pylint: disable=no-value-for-parameter
            )[0]
        return str(name)

    def Popen(self, cmdargs=None, **options):
        """
        Create a ``subprocess`` for this Node.js command.

        :param cmdargs:
            Optional sequence of command argument strings.
        :param options:
            General options for ``zetup.call``, including all options for
            ``subprocess.call``.
        """
        command = [str(self)]
        if cmdargs is not None:
            command += cmdargs
        return zetup.Popen(command, **options)

    def call(self, cmdargs=None, **options):
        """
        Call this Node.js command.

        :param cmdargs:
            Optional sequence of command argument strings.
        :param options:
            General options for ``zetup.call``, including all options for
            ``subprocess.call``.
        """
        command = [str(self)]
        if cmdargs is not None:
            command += cmdargs
        return zetup.call(command, **options)

    def check_call(self, cmdargs=None, **options):
        """
        Call this Node.js command and check its return code.

        :param cmdargs:
            Optional sequence of command argument strings.
        :param options:
            General options for ``zetup.call``, including all options for
            ``subprocess.call``.

        :raises subprocess.CalledProcessError:
            When return code is not zero.
        """
        command = [str(self)]
        if cmdargs is not None:
            command += cmdargs

        returncode = zetup.call(command, **options)
        if returncode:
            raise NodeCommandError(returncode, command, os.getcwd())

    def check_output(self, cmdargs=None, **options):
        """
        Call this Node.js command, check return code, and return its stdout.

        :param cmdargs:
            Optional sequence of command argument strings.
        :param options:
            General options for ``zetup.call``, including all options for
            ``subprocess.call``.

        :raises subprocess.CalledProcessError:
            When return code is not zero.
        """
        command = [str(self)]
        if cmdargs is not None:
            command += cmdargs

        process = zetup.Popen(command, stdout=PIPE, **options)
        out, _ = process.communicate()
        if process.returncode:
            raise NodeCommandError(process.returncode, command, os.getcwd())

        return out

    def __call__(self, *cmdargs, **kwargs):
        """
        Alternative to :meth:`.check_output`.

        Takes `cmdargs` as varargs instead of a sequence parameter
        """
        return self.check_output(cmdargs, **kwargs)

    def __repr__(self):
        return "{}[{!r}]".format(__name__, self.name)
