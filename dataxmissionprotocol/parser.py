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
      self.__handlers = {}
      self.__format = format
      self.__defaultPacketType = defaultPacketType
   
   def addHandler(self, handler):
      self.__handlers[handler.packetType.CMD] = handler
      
      return self
   
   def parse(self, data):
      packets = []
      
      self.__buf.extend(data)
      
      offset = 0
      
      while True:
         try:
            offset = self.__format.getPacketStartIndex(self.__buf, offset)
         
         except ValueError:
            offset = len(self.__buf)
            break
         
         if not self.__format.hasEnoughBytes(self.__buf, offset):
            break
         
         packetSize = self.__format.getPacketSize(self.__buf, offset)
         
         handler = self.__handlers.get(self.__format.getCommandNumber(self.__buf, offset))
         
         try:
            packet = (handler.packetType if handler else self.__defaultPacketType)(self.__format).wrap(self.__buf, start = offset, end = offset + packetSize)
         
         except ValueError:
            offset += 1
         
         else:
            if handler and handler.handler:
               handler.handler(packet)
               
            else:
               packets.append(packet)
            
            offset += packetSize
      
      del self.__buf[0:offset]
      
      return packets
