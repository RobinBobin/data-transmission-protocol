from . import Formats
from .simpleformat import SimpleFormat
from ..field import Field

marker = Field(1, False)
marker.value = 0x55

size = Field(1, False, marker)
cmd = Field(1, False, size)

Formats.zx55v1 = SimpleFormat(marker, size, cmd, Field(2, False))
