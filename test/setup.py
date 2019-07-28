import os
import sys

from setuptools import setup


TEST_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(TEST_DIR, 'variables.py')) as varfile:
    exec(varfile.read())


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
    require_node_modules=[
        NODE_PACKAGE,  # pylint: disable=undefined-variable
    ],
)
