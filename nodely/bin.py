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

from types import ModuleType
import platform
import sys

from path import Path
import zetup

from nodely import NODE_MODULES_DIR

__all__ = ['Command']


#: Running on Windows?
WIN = platform.system() == 'Windows'


#: The original nodely.bin module object
ORIGIN = sys.modules[__name__]


class Module(ModuleType):
    """
    Wrapper module class for :mod:`nodely.bin`

    Makes module directly act as command proxy to the ``node_modules/.bin/``
    directory via :meth:`.__getitem__` and :meth:`.__getattr__`
    """

    def __init__(self):
        """
        Get ``__name__`` and ``__doc__`` and update ``.__dict__`` from
        original ``nodely.bin`` module
        """
        super(Module, self).__init__(__name__, ORIGIN.__doc__)
        self.__dict__.update(ORIGIN.__dict__)

    def __getitem__(self, cmdname):
        """
        Get a :class:`nodely.bin.Command` instance for given `cmdname`

        :raises OSError: if executable can not be found
        """
        return Command(cmdname)

    def __getattr__(self, name):
        """
        Get a :class:`nodely.bin.Command` instance for given command `name`

        :raises OSError: if executable can not be found
        """
        try:  # first check if original module has the given attribute
            return getattr(ORIGIN, name)
        except AttributeError:
            pass
        # and don't treat special Python member names as Node.js commands
        if name.startswith('__'):
            raise AttributeError("{!r} has no attribute {!r}"
                                 .format(self, name))
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
    A Node.js executable from ``node_modules/.bin/`` of current Python
    environment
    """

    def __new__(cls, name):
        """
        Check existance an store absolute path in ``path.Path`` base

        :param name:
           The basename of the executable in ``node_modules/.bin``
        :raises OSError:
           if executable can not be found
        """
        if WIN:  # pragma: no cover
            name += '.cmd'
        cmd = Path.__new__(cls, NODE_MODULES_DIR / '.bin' / name)
        cmd.atime  # HACK: raises OSError if not existing
        return cmd

    def __init__(self, name):
        """
        :meth:`.__new__` does all the work :)
        """
        pass

    @property
    def name(self):
        """
        The name of this Node.js command
        """
        name = Path(self).basename()
        if WIN:  # pragma: no cover
            # remove .cmd file extension
            name = name.splitext()[0]
        return str(name)

    def Popen(self, cmdargs=None, **kwargs):
        """
        Create a ``subprocess`` for this Node.js command with optional
        sequence of `cmdargs` strings and optional `kwargs` for
        ``zetup.Popen``, including all options for ``subprocess.Popen``
        """
        command = [str(self)]
        if cmdargs is not None:
            command += cmdargs
        return zetup.Popen(command, **kwargs)

    def call(self, cmdargs=None, **kwargs):
        """
        Call this Node.js command with optional sequence of `cmdargs` strings
        and optional `kwargs` for ``zetup.call``, including all options for
        ``subprocess.call``
        """
        command = [str(self)]
        if cmdargs is not None:
            command += cmdargs
        return zetup.call(command, **kwargs)

    def __call__(self, cmdargs=None, **kwargs):
        """
        Alternative to :meth:`.call`
        """
        return self.call(cmdargs, **kwargs)

    def __repr__(self):
        return "{}[{!r}]".format(__name__, self.name)
