"""Setup for Python ``nodely`` package distribution."""

from __future__ import print_function

from setuptools import setup


dist = None
try:
    dist = setup(
        setup_requires=open("requirements.setup.txt").read(),

        use_zetup=True,

        entry_points={'distutils.setup_keywords': [
            "require_node_modules="
            "nodely.setup_keywords:require_node_modules",
        ]},
    )

finally:
    if dist is not None and hasattr(dist, 'zetup_made'):
        dist.zetup_made.clean()
