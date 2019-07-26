"""nodely exceptions."""

from subprocess import CalledProcessError

__all__ = ('NodeCommandError', )


class NodeCommandError(CalledProcessError):
    """A Node.js command returned non-zero exit code"""

    def __init__(self, returncode, cmd, cwd):
        super().__init__(returncode=returncode, cmd=cmd)
        self.cwd = cwd
        self.args += (cwd, )

    def __str__(self):
        return "{} in working directory {!r}".format(
            super().__str__(), self.cwd)
