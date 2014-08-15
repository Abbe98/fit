from fit.io.reader import Reader
from fit.io.writer import Writer
from fit.message import Message
from fit.mixin import KNOWN as KNOWN_MIXINS
from fit.structure.body import Body


class FitFile(object):
    def __init__(self, fd, body=None):
        self._fd = fd

        self.body = body or Body()
        self._apply_mixin()

    @classmethod
    def open(cls, filename, mode='r'):
        if mode not in 'rwa':
            raise ValueError(
                "mode string must be one of 'r', 'w' or 'a', not '%s'" % mode)

        fd = open(filename, mode='%sb' % 'w' if mode == 'w' else 'r')

        body = None
        if mode in 'ar':
            body = Reader(fd).body

        if mode == 'a':
            fd.close()
            fd = open(filename, mode='ab')

        return cls(fd, body=body)

    def __repr__(self):
        return "<%s '%s', mode '%s'>" % (
            self.__class__.__name__,
            self.name, self.mode[0]
        )

    def __del__(self):
        return self.close()

    # File I/O methods

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_val:
            return self.close()

        raise exc_type, exc_val, exc_tb

    @property
    def mode(self):
        return self._fd.mode

    @property
    def name(self):
        return self._fd.name

    @property
    def closed(self):
        return self._fd.closed

    def fileno(self):
        return self._fd.fileno()

    def isatty(self):
        return self._fd.isatty()

    def readable(self):
        return self.mode[0] in 'ar'

    def seekable(self):
        return False

    def writable(self):
        return self.mode[0] in 'aw'

    def flush(self):
        if not self.writable():
            return

        Writer(self._fd, body=self.body).write()

    def close(self):
        if self.closed:
            return

        self.flush()
        self._fd.close()

    def minimize(self):
        self.body = self.body.compressed

    # List special methods

    def __getitem__(self, i):
        return self.body[i]

    def __setitem__(self, i, value):
        self.body[i] = value
        self._apply_mixin()

    def __delitem__(self, i):
        del self.body[i]
        self._apply_mixin()

    def __iter__(self):
        for item in self.body:
            yield item

    def __len__(self):
        return len(self.body)

    def append(self, value):
        self.body.append(value)
        self._apply_mixin()

    def extend(self, values):
        self.body.extend(values)
        self._apply_mixin()

    def remove(self, i):
        self.body.remove(i)
        self._apply_mixin()

    def pop(self, i=None):
        value = self.body.pop(i)
        self._apply_mixin()
        return value

    def index(self, i):
        return self.body.index(i)

    # FIT special methods

    def _apply_mixin(self):
        mixin_cls = None
        if self.body.file_id:
            mixin_cls = KNOWN_MIXINS.get(self.body.file_id.type)
        if mixin_cls:
            self.__class__ = type(
                mixin_cls.__name__, (FitFile, mixin_cls), {})

    def copy(self, other):
        assert isinstance(other, FitFile)
        self.body = other.body
        self._apply_mixin()
