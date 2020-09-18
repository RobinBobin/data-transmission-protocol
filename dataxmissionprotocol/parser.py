from commonutils import StaticUtils
from inspect import signature
from .packet import Packet

class Parser:
   class Handler:
      def __init__(self, packetType, handler):
         self.__packetType = packetType
         self.__handler = handler
      
      @property
      def packetType(self):
         return self.__packetType
      
      @property
      def handler(self):
         return self.__handler
   
   def __init__(self, fmt, defaultPacketType = Packet):
      self.__buf = bytearray()
      self.__defaultHandler = None
      self.__defaultPacketType = defaultPacketType
      self.__defaultParameterCount = len(signature(defaultPacketType.__init__).parameters)
      self.__format = fmt
      self.__handlers = {}
      self.__interPacketBytes = 0
      self.__postPacketBytes = 0
      self.__prePacketBytes = 0
      self.__processed = 0
      self.__trustValidity = False
   
   @property
   def format(self):
      return self.__format
   
   @property
   def postPacketBytes(self):
      return self.__postPacketBytes
   
   @postPacketBytes.setter
   def postPacketBytes(self, postPacketBytes):
      self.__setPrePostPacketBytes(False, postPacketBytes)
   
   @property
   def prePacketBytes(self):
      return self.__prePacketBytes
   
   @prePacketBytes.setter
   def prePacketBytes(self, prePacketBytes):
      self.__setPrePostPacketBytes(True, prePacketBytes)
   
   @property
   def processed(self):
      return self.__processed
   
   @property
   def trustValidity(self):
      return self.__trustValidity
   
   @trustValidity.setter
   def trustValidity(self, trustValidity):
      StaticUtils.confirm(trustValidity or not self.__interPacketBytes, "'trustValidity' can't be False if interpacket data is stored")
      
      self.__trustValidity = trustValidity
   
   def addHandler(self, handler):
      cmd = None
      
      if isinstance(handler.packetType, Packet):
         cmd = handler.packetType.CMD
      
      else:
         cmd = handler.packetType
         handler = Parser.Handler(self.__defaultPacketType, handler.handler)
      
      self.__handlers[cmd] = handler
      
      return self
   
   def parse(self, data):
      chunks = None if self.__defaultHandler else []
      
      self.__buf.extend(data)
      
      offset = 0
      
      while True:
         initialOffset = offset
         searchOffset = initialOffset + self.__prePacketBytes
         packetFound = True # For future versions.
         
         try:
            offset = self.__format.getPacketStartIndex(self.__buf, searchOffset)
         
         except ValueError:
            if not self.__interPacketBytes:
               offset = len(self.__buf)
            
            break
         
         StaticUtils.confirm((not self.__prePacketBytes) or (offset == searchOffset), "Data validity is compromised")
         
         packetSize = self.__format.getPacketSize(self.__buf, offset, safely = True) if packetFound else 0
         
         chunkSize = packetSize + self.__postPacketBytes
         
         if (packetFound and not packetSize) or ((len(self.__buf) - offset) < chunkSize):
            offset = initialOffset
            break
         
         handler = self.__handlers.get(self.__format.getCommandNumber(self.__buf, offset))
         
         packetType = handler.packetType if handler else self.__defaultPacketType
            
         parameterCount = self.__defaultParameterCount if packetType == self.__defaultPacketType else len(signature(packetType.__init__).parameters)
         
         try:
            packet = (packetType() if parameterCount == 2 else packetType(self.__format)).wrap(self.__buf, start = offset, end = offset + packetSize, trustValidity = self.__trustValidity) if packetFound else None
         
         except ValueError:
            offset += 1
         
         else:
            handler = handler.handler if handler and handler.handler else self.__defaultHandler
            
            postPacketBytesOffset = initialOffset + self.__prePacketBytes + packetSize
            
            chunkData = (
               packet                     \
               , self.__buf               \
               , initialOffset            \
               , self.__prePacketBytes    \
               , postPacketBytesOffset    \
               , self.__postPacketBytes
            ) if self.__interPacketBytes else (packet, )
            
            if handler:
               handler(*chunkData)
            
            else:
               chunks.append(chunkData)
            
            offset += chunkSize
      
      self.__processed += offset
      
      del self.__buf[0:offset]
      
      return chunks
   
   def resetProcessed(self):
      self.__processed = 0
   
   def setDefaultHandler(self, handler):
      self.__defaultHandler = handler
      
      return self
   
   def __setPrePostPacketBytes(self, preOrPost, newValue):
      StaticUtils.confirm(not newValue or self.__trustValidity, "Interpacket data can't be stored if 'trustValidity' is False")
      
      if preOrPost:
         self.__prePacketBytes = newValue
      
      else:
         self.__postPacketBytes = newValue
      
      self.__interPacketBytes = self.__prePacketBytes + self.__postPacketBytes
