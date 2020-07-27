from serial import serial_for_url
from serial.serialutil import portNotOpenError
from .protocol import Protocol
from .readerthread import ReaderThread
from .. import Port
from ..queue import ConnectionEstablished

class Serial(Port):
   def __init__(self, parser, protocolFactory = Protocol):
      super().__init__(parser, portNotOpenError)
      
      self.__baudrate = 9600
      self.__protocolFactory = protocolFactory
      self.__thread = None
      self.__timeout = None
   
   @property
   def baudrate(self):
      return self.__baudrate
   
   @baudrate.setter
   def baudrate(self, baudrate):
      self.__baudrate = baudrate
   
   @property
   def timeout(self):
      return self.__timeout
   
   @timeout.setter
   def timeout(self, timeout):
      self.__timeout = timeout
   
   def isOpen(self):
      return self.__thread and self.__thread.serial.is_open
   
   def _close(self):
      if self.__thread:
         self.__thread.close()
         self.__thread = None
   
   def _open(self, path = None, **kw):
      if path is None:
         path = self.path
      
      for key in ("baudrate", "timeout"):
         if key in kw:
            setattr(self, key, kw[key])
         
         else:
            kw[key] = getattr(self, key)
      
      self.__thread = ReaderThread(self, serial_for_url(path, **kw), self.__protocolFactory)
      
      self.__thread.start()
      self.__thread.connect()
      
      self.addQueueItem(ConnectionEstablished())
   
   def _write(self, packet):
      self.__thread.serial.write(packet.rawBuffer)
