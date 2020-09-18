from . import Formats
from .simpleformat import SimpleFormat
from ..field import UnsignedField1, UnsignedField2

marker = UnsignedField1(0x55)
size = UnsignedField1(previousField = marker)
cmd = UnsignedField1(previousField = size)

Formats.zx55v1 = SimpleFormat(marker, size, cmd, UnsignedField2())
