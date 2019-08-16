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
nodely

putMORE Node.js into Python
"""

import json
import os
import sys

from path import Path
from pkg_resources import get_distribution
import whichcraft
import zetup

from .error import NodeCommandError

# HACK: Fix inconsistently hard-coded whichcraft.__version__
whichcraft.__version__ = get_distribution('whichcraft').version

zetup.toplevel(__name__, [
    'NodeCommandError',
    'Popen',
    'call',
    'install',
    'uninstall',
    'which',
])


#:  The absolute path to the local ``node_modules/`` sub-directory.
#
#   Which is located under the current Python environment root, and which is
#   used for installing Node.js packages into
NODE_MODULES_DIR = (Path(sys.prefix) / 'node_modules').mkdir_p()

# create a dummy package.json in python environment root for making npm
# install packages to node_modules/ sub-directory defined above
(Path(sys.prefix) / 'package.json').write_text(json.dumps({
    'name': "python-nodely",
    'description': "putMORE Node.js into Python",
    'repository': "https://github.com/zimmermanncode/nodely",
}))

# and make sure that the node_modules/.bin/ dir always exists
(NODE_MODULES_DIR / '.bin').mkdir_p()


def install(package):
    """
    Install given Node.js `package`.

    Into ``node_modules/`` of current Python environment
    """
    command = ['npm', 'install', package]
    with Path(sys.prefix):
        status = zetup.call(command)
    if status:
        raise NodeCommandError(command, status, os.getcwd())


def uninstall(package):
    """
    Uninstall given Node.js `package`.

    From ``node_modules/`` of current Python environment
    """
    command = ['npm', 'uninstall', package]
    with Path(sys.prefix):
        status = zetup.call(command)
    if status:  # pragma: no cover
        raise NodeCommandError(command, status, os.getcwd())


def which(executable):
    """
    Find `executable` in ``node_modules/.bin/`` of current Python environment.

    :return: Absolute ``path.Path`` instance or ``None``
    """
    path = whichcraft.which(executable, path=NODE_MODULES_DIR / '.bin')
    if path is not None:
        return Path(path)


def Popen(executable, args=None, **kwargs):
    """
    Create a subprocess for given Node.js `executable`.

    :param args:
        Optional sequence of command argument strings
    :param options:
        General options for ``zetup.call``, including all options for
        ``subprocess.call``
    """
    import nodely.bin

    command = nodely.bin[executable]
    return command.Popen(args, **kwargs)


def call(executable, args=None, **kwargs):
    """
    Call given Node.js `executable`.

    :param args:
        Optional sequence of command argument strings
    :param kwargs:
        General options for ``zetup.call``, including all options for
        ``subprocess.call``
    """
    import nodely.bin

    command = nodely.bin[executable]
    return command.call(args, **kwargs)
