from functools import reduce
from struct import unpack_from
from .field import Field

class Packet:
   def __init__(self, fmt, **kw):
      self.__buf = []
      self.__format = fmt
      
      # = "cmd" can be missing, if we want to wrap() = #
      if "cmd" in kw:
         d = {key: key in kw for key in ("size", "params", "fields")}
         sizeSpecified, paramsSpecified, fieldsSpecified = d.values()
         
         if list(d.values()).count(True) > 1:
            raise ValueError(f"Only one of {list(d.keys())} can be specified")
         
         self.__buf = bytearray([0] * fmt.minPacketSize)
         
         def extendBuf(size):
            self.__buf.extend(bytearray([0] * size))
         
         if sizeSpecified:
            extendBuf(kw["size"])
         
         elif paramsSpecified:
            self.__buf[fmt.paramsOffset : fmt.paramsOffset] = kw["params"]
         
         elif fieldsSpecified:
            fields = kw["fields"]
            extendBuf(reduce(lambda x, y: x + y, map(lambda f: f.size, fields)))
            self.setParams(fields = fields)
         
         fmt.setCommandNumber(self.__buf, kw["cmd"])
         fmt.finalizePacket(self.__buf)
   
   def __str__(self):
      return f"<{self.__class__.__name__}, {list(self.rawBuffer)}>"
   
   def getParam(self, param):
      return self.__format.getParam(self.__buf, param)
   
   def getParams(self, structFormat):
      return unpack_from(structFormat, self.__buf, self.__format.paramsOffset)
   
   def setParam(self, param, finalize = False):
      self.__format.setParam(self.__buf, param, finalize)
   
   def setParams(self, values = None, signed = None, size = None, fields = None):
      fields = Field.createChain(size, signed, values, fields)
      
      for index, field in enumerate(fields):
         self.setParam(field, index == (len(fields) - 1))
   
   def wrap(self, buffer, **kw):
      if not isinstance(buffer, bytearray):
         buffer = bytearray(buffer)
      
      self.__buf = buffer[kw.get("start", 0):kw.get("end", len(buffer))]
      
      isValid = kw.get("trustValidity", False) or self.__format.isValid(self.__buf)
      
      if not isValid:
         raise ValueError(f"{self.__buf} is not a valid packet.")
      
      return self
   
   @property
   def commandNumber(self):
      return self.__format.getCommandNumber(self.__buf)
   
   @property
   def size(self):
      return self.__format.getPacketSize(self.__buf) - self.__format.minPacketSize
   
   @property
   def rawBuffer(self):
      return self.__buf
   
   def _verifyCmdValidity(self, cmd):
      commandNumber = self.commandNumber
      
      if commandNumber != cmd:
         raise AssertionError(f"{self.__class__.__name__}: the command number must be {cmd}, not {commandNumber}.")
   
   def _verifySizeValidity(self, size):
      packetSize = self.__format.getPacketSize(self.__buf)
      
      if len(self.__buf) != packetSize:
         raise AssertionError(f"{self.__class__.__name__}: the internal buffer length ({len(self.__buf)}) isn't equal to the packet size stored in it ({packetSize}).")
      
      totalSize = size + self.__format.minPacketSize
      
      if packetSize != totalSize:
         raise AssertionError(f"{self.__class__.__name__}: the packet size must be {totalSize}, not {packetSize}.")
