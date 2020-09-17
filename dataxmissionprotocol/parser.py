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
   
   def __init__(self, format, defaultPacketType = Packet):
      self.__buf = bytearray()
      self.__defaultHandler = None
      self.__defaultPacketType = defaultPacketType
      self.__defaultParameterCount = len(signature(defaultPacketType.__init__).parameters)
      self.__format = format
      self.__handlers = {}
      self.__trustValidity = False
   
   @property
   def format(self):
      return self.__format
   
   @property
   def trustValidity(self):
      return self.__trustValidity
   
   @trustValidity.setter
   def trustValidity(self, trustValidity):
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
      packets = None if self.__defaultHandler else []
      
      self.__buf.extend(data)
      
      offset = 0
      
      while True:
         try:
            offset = self.__format.getPacketStartIndex(self.__buf, offset)
         
         except ValueError:
            offset = len(self.__buf)
            break
         
         packetSize = self.__format.getPacketSize(self.__buf, offset, safely = True)
         
         if not packetSize:
            break
         
         handler = self.__handlers.get(self.__format.getCommandNumber(self.__buf, offset))
         
         try:
            packetType = handler.packetType if handler else self.__defaultPacketType
            
            parameterCount = self.__defaultParameterCount if packetType == self.__defaultPacketType else len(signature(packetType.__init__).parameters)
            
            packet = (packetType() if parameterCount == 2 else packetType(self.__format)).wrap(self.__buf, start = offset, end = offset + packetSize, trustValidity = self.__trustValidity)
         
         except ValueError:
            offset += 1
         
         else:
            h = handler.handler if handler and handler.handler else self.__defaultHandler
            
            if h:
               h(packet)
            
            else:
               packets.append(packet)
            
            offset += packetSize
      
      del self.__buf[0:offset]
      
      return packets
   
   def setDefaultHandler(self, handler):
      self.__defaultHandler = handler
      
      return self
