"""nodely exceptions."""

from subprocess import CalledProcessError

import zetup

import nodely

__all__ = ('NodeCommandError', )


class NodeCommandError(CalledProcessError, zetup.object):
    """A Node.js command returned non-zero exit code"""

    __package__ = nodely

    def __init__(self, returncode, cmd, cwd):
        super(NodeCommandError, self).__init__(
            returncode=returncode, cmd=cmd)
        self.cwd = cwd
        self.args += (cwd, )

    def __str__(self):
        return "{} in working directory {!r}".format(
            super(NodeCommandError, self).__str__().rstrip("."), self.cwd)
