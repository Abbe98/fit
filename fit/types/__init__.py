from struct import unpack, pack

from fit.utils import get_known


class Type(object):
    type = -1
    size = 0
    format = "x"

    _invalid = None

    def __init__(self, number, size=None):
        self.number = number
        self.size = size or self.__class__.size

    def __eq__(self, other):
        return self.number == other.number

    def __repr__(self):
        return '<%s[%d]>' % (
            self.__class__.__name__, self.number
        )

    def read(self, buffer, architecture="<"):
        data = unpack("%(arch)s%(format)s" % {
            "arch": architecture,
            "format": self.format
        }, buffer.read(self.size))[0]

        if data == self._invalid:
            data = None

        return self._load(data) if data is not None else None

    def write(self, value):
        return pack(
            "<%s" % self.format,
            self._save(value) if value is not None else self._invalid)

    def _load(self, data):
        return data

    def _save(self, value):
        return value


class KnownMixin(object):
    known = {}

    def _load(self, data):
        return self.known.get(data, data)

    def _save(self, value):
        for key, value in self.known.items():
            if value == value:
                return key
        return value


KNOWN = get_known(__name__, Type)
