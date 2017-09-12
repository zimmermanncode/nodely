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
nodely entry points for ``distutils.setup_keywords``.

Adding ``require_node_modules`` to ``setup()``::

   from setuptools import setup

   setup(
       ...
       setup_requires=['nodely', ...],
       require_node_modules=['coffee-script', ...],
       ...
   )
"""

from moretools import isstring

import nodely

__all__ = ('require_node_modules', )


def require_node_modules(dist, keyword='require_node_modules',
                         jsmodules=None):
    """
    Install required `jsmodules` during a Python package ``setup()``.
    """
    assert keyword == 'require_node_modules'
    if jsmodules is None:
        return

    if isstring(jsmodules):
        jsmodules = filter(
            None, (mod.strip() for mod in jsmodules.split('\n')))
    for jsmod in jsmodules:
        nodely.install(jsmod)
