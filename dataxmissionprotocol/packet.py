from .field import Field

class Packet:
   def __init__(self, format, **kwargs):
      self.__format = format
      
      if "cmd" in kwargs:
         sizeSpecified = "size" in kwargs
         paramsSpecified = "params" in kwargs
         
         if sizeSpecified and paramsSpecified:
            raise ValueError("Either 'params' or 'size' can be specified.")
         
         self.__buf = bytearray([0] * format.minPacketSize)
         
         if sizeSpecified:
            self.__buf.extend(bytearray([0] * kwargs["size"]))
         
         elif paramsSpecified:
            self.__buf[format._paramsOffset : format._paramsOffset] = kwargs["params"]
         
         format.setCommandNumber(self.__buf, kwargs["cmd"])
         format.finalizePacket(self.__buf)
   
   def wrap(self, buffer, **kwargs):
      if not isinstance(buffer, bytearray):
         buffer = bytearray(buffer)
      
      self.__buf = buffer[kwargs.get("start", 0):kwargs.get("end", len(buffer))]

      if not self.__format.isValid(self.__buf):
         raise ValueError(f"{self.__buf} is not a valid packet.")
      
      return self
   
   def getParam(self, param):
      return self.__format.getParam(self.__buf, param)
   
   def setParam(self, param, finalize = False):
      self.__format.setParam(self.__buf, param, finalize)
   
   def setParams(self, values = None, signed = None, size = None, fields = None):
      fields = Field.createChain(size, signed, values, fields)
      
      for index, field in enumerate(fields):
         self.setParam(field, index == (len(fields) - 1))
   
   @property
   def size(self):
      return self.__format.getPacketSize(self.__buf) - self.__format.minPacketSize
   
   @property
   def rawBuffer(self):
      return self.__buf
   
   def _verifyCmdValidity(self, cmd):
      commandNumber = self.__format.getCommandNumber(self.__buf)
      
      if commandNumber != cmd:
         raise AssertionError(f"{self.__class__.__name__}: the command number must be {cmd}, not {commandNumber}.")
   
   def _verifySizeValidity(self, size):
      packetSize = self.__format.getPacketSize(self.__buf)
      
      if len(self.__buf) != packetSize:
         raise AssertionError(f"{self.__class__.__name__}: the internal buffer length ({len(self.__buf)}) isn't equal to the packet size stored in it ({packetSize}).")
      
      totalSize = size + self.__format.minPacketSize
      
      if packetSize != totalSize:
         raise AssertionError(f"{self.__class__.__name__}: the packet size must be {totalSize}, not {packetSize}.")
