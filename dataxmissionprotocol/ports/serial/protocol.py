from serial.threaded import Protocol as ProtocolBase
from ..queue import ConnectionEstablished, ConnectionLost, DataReceived

class Protocol(ProtocolBase):
   def connection_made(self, transport):
      self.__port = transport.port
      
      self.__port.addQueueItem(ConnectionEstablished())
   
   def data_received(self, data):
      self.__port.addQueueItem(DataReceived(data))
   
   def connection_lost(self, exc):
      self.__port.addQueueItem(ConnectionLost(exc))
