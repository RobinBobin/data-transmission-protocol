from serial import serial_for_url
from serial.serialutil import SerialException, portNotOpenError
from .protocol import Protocol
from .readerthread import ReaderThread
from .. import Port

class Serial(Port):
   def __init__(self, parser, protocolFactory = Protocol):
      super().__init__(parser, portNotOpenError, SerialException)
      
      self.__protocolFactory = protocolFactory
      self.__thread = None
   
   def isOpen(self):
      return self.__thread and self.__thread.serial.is_open
   
   def _close(self):
      if self.__thread:
         self.__thread.close()
         self.__thread = None
   
   def _open(self, path, **kw):
      self.__thread = ReaderThread(self, serial_for_url(path, **kw), self.__protocolFactory)
      
      self.__thread.start()
      self.__thread.connect()
   
   def _write(self, packet):
      self.__thread.serial.write(packet.rawBuffer)
