import os

from setuptools import setup


ROOT = os.path.dirname(os.path.realpath(__file__))


setup(
    name='nodely',
    description="putMORE Node.js into Python",

    author="Stefan Zimmermann",
    author_email="user@zimmermann.co",
    url="https://github.com/zimmermanncode/nodely",

    license='LGPLv3',

    setup_requires=open(os.path.join(ROOT, 'requirements.setup.txt')).read(),
    install_requires=open(os.path.join(ROOT, 'requirements.txt')).read(),

    use_scm_version={
        'local_scheme': lambda _: '',
        'write_to': 'nodely/__version__.py',
    },
    packages=[
        'nodely',
    ],
    entry_points={'distutils.setup_keywords': [
        'require_node_modules = nodely.setup_keywords:require_node_modules',
    ]},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved'
        ' :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    keywords=[
        'nodely', 'nodejs', 'node', 'npm', 'npmjs',
        'nodejspackages', 'nodejspackage', 'nodejsmodules', 'nodejsmodule',
        'nodepackages', 'nodepackage', 'nodemodules', 'nodemodule',
        'npmpackages', 'npmpackage', 'npmmodules', 'npmmodule',
        'packages', 'package', 'nodemodules', 'modules', 'module', 'bin',
        'javascript', 'js', 'ecmascript', 'ecma', 'es',
        'install', 'uninstall', 'which', 'subprocess', 'popen', 'call',
        'more', 'tools', 'tool',
    ],
)
