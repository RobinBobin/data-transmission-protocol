class BaseFormat:
   __byteorder = {
      None: "=",
      "little": "<",
      "big": ">"
   }
   
   def __init__(self):
      self.__byteorder = None
      self._minPacketSize = None
   
   @property
   def byteorder(self):
      return self.__byteorder
   
   @byteorder.setter
   def byteorder(self, byteorder):
      if byteorder not in BaseFormat.__byteorder.keys():
         raise ValueError() if isinstance(byteorder, str) else TypeError
      
      self.__byteorder = byteorder
   
   @property
   def minPacketSize(self):
      return self._minPacketSize
   
   def hasEnoughBytes(self, buf, offset):
      return (len(buf) - offset) >= self._minPacketSize
   
   def readField(self, buf, offset, field):
      field._read(buf, offset, BaseFormat.__byteorder[self.__byteorder])
   
   def writeField(self, buf, offset, field):
      field._write(buf, offset, BaseFormat.__byteorder[self.__byteorder])
