from serial.threaded import Protocol as ProtocolBase
from ..queue import ConnectionLost, DataReceived

class Protocol(ProtocolBase):
   def connection_made(self, transport):
      self.__port = transport.port
   
   def data_received(self, data):
      if self.__port.debugRead:
         print(list(data))
      
      self.__port.addQueueItem(DataReceived(data))
   
   def connection_lost(self, exc):
      self.__port.addQueueItem(ConnectionLost(exc))
