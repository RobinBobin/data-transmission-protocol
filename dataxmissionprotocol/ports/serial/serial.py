from serial import serial_for_url
from serial.serialutil import SerialException, portNotOpenError
from .protocol import Protocol
from .readerthread import ReaderThread
from .. import Port

class Serial(Port):
   def __init__(self, parser, protocolFactory = Protocol):
      super().__init__(parser)
      
      self.__protocolFactory = protocolFactory
      self.__thread = None
   
   def close(self):
      if self.__thread:
         self.__thread.close()
         self.__thread = None
   
   def open(self, path, **kw):
      self.close()
      
      try:
         self.__thread = ReaderThread(self, serial_for_url(path, **kw), self.__protocolFactory)
         
         self.__thread.start()
         self.__thread.connect()
         
         return True
      
      except SerialException as e:
         self.errorProcessor(e)
