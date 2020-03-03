from . import Formats
from .simpleformat import SimpleFormat
from ..field import Field

marker = Field(1, signed = False, value = 0x55)
size = Field(2, signed = False, previousField = marker)
cmd = Field(1, signed = False, previousField = size)

Formats.zx55v2 = SimpleFormat(marker, size, cmd, Field(2, signed = False))
