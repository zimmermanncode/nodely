import os  # pragma: no coverage
import sys  # pragma: no coverage

from setuptools import setup  # pragma: no coverage


TEST_DIR = os.path.dirname(  # pragma: no coverage
    os.path.realpath(__file__))

with open(
        os.path.join(TEST_DIR, 'variables.py')
) as varfile:  # pragma: no coverage
    exec(varfile.read())


setup(  # pragma: no coverage
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
