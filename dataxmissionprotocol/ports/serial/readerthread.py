from serial.threaded import ReaderThread as ReaderThreadBase

class ReaderThread(ReaderThreadBase):
   def __init__(self, port, serial_instance, protocol_factory):
      super().__init__(serial_instance, protocol_factory)
      
      self.__port = port
   
   @property
   def port(self):
      return self.__port
