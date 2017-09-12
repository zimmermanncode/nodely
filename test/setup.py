import os
import sys

from setuptools import setup


ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, ROOT)

import conftest


setup(
    name='nodely-test',
    description="Test puttingMORE Node.js into Python",

    author="Stefan Zimmermann",
    author_email="user@zimmermann.co",
    url="https://github.com/zimmermanncode/nodely",

    license='LGPLv3',

    setup_requires=['setuptools_scm', 'nodely'],

    use_scm_version={
        'root': '..',
        'local_scheme': lambda _: '',
    },
    require_node_modules=[conftest.node_package()],
)
