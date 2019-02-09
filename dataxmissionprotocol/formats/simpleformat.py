from .baseformat import BaseFormat

class SimpleFormat(BaseFormat):
   def __init__(self, marker, size, cmd, crc):
      super().__init__()
      
      if marker.size > 1:
         raise NotImplementedError()
      
      self._minPacketSize = marker.size + size.size + cmd.size + crc.size
      
      self.__marker = marker
      self.__size = size
      self.__cmd = cmd
      self.__paramsOffset = cmd.nextOffset
      self.__crc = crc
   
   def hasEnoughBytes(self, buf, offset):
      return super().hasEnoughBytes(buf, offset) and remaining >= self.getPacketSize(buf, offset)
