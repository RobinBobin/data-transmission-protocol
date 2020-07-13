from .baseformat import BaseFormat

class SimpleFormat(BaseFormat):
   def __init__(self, marker, size, cmd, crc):
      super().__init__()
      
      if marker.size > 1:
         # see self.getPacketStartIndex() implementation.
         raise NotImplementedError()
      
      self._minPacketSize = marker.size + size.size + cmd.size + crc.size
      
      self.__marker = marker
      self.__size = size
      self.__cmd = cmd
      self._paramsOffset = cmd.nextOffset
      self.__crc = crc
   
   def getMaxPacketSize(self):
      return 2 ** (self.__size.size * 8) - 1 - self.minPacketSize
   
   def getPacketStartIndex(self, buf, offset):
      return buf.index(self.__marker.value, offset)
   
   def getTotalPacketSize(self, size):
      return size + self.minPacketSize
   
   def hasEnoughBytes(self, buf, offset):
      return super().hasEnoughBytes(buf, offset) and (len(buf) - offset) >= self.getPacketSize(buf, offset)
   
   def getPacketSize(self, buf, offset = 0):
      return self._getField(buf, offset, self.__size).value
   
   def getCommandNumber(self, buf, offset = 0):
      return self._getField(buf, offset, self.__cmd).value
   
   def getParam(self, buf, param):
      return self._getField(buf, self._paramsOffset, param)
   
   def isValid(self, buf):
      if len(buf) < self.minPacketSize or self._getField(buf, 0, self.__marker).value != self.__marker.value:
         return False
      
      packetSize = self.getPacketSize(buf)
      self.__crc.offset = packetSize - self.__crc.size
      
      return packetSize >= self.minPacketSize   \
         and len(buf) == packetSize             \
         and self._getField(buf, 0, self.__crc).value == self._calcCrc(buf)
   
   def setCommandNumber(self, buf, commandNumber):
      self.__cmd.value = commandNumber
      
      self._setField(buf, 0, self.__cmd)
   
   def setParam(self, buf, param, finalize = False):
      self._setField(buf, self._paramsOffset, param)
      
      if finalize:
         self.finalizePacket(buf)
   
   def finalizePacket(self, buf):
      self._setField(buf, 0, self.__marker)
      
      self.__size.value = len(buf)
      self._setField(buf, 0, self.__size)
      
      self.__crc.offset = self.__size.value - self.__crc.size
      self.__crc.value = self._calcCrc(buf)
      self._setField(buf, 0, self.__crc)
   
   def _calcCrc(self, buf):
      crc = 0
      
      for i in range(self.__size.offset, len(buf) - self.__crc.size):
         crc += buf[i]
      
      return crc
