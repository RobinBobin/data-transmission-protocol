from commonutils import StaticUtils
from queue import Empty, SimpleQueue
from .connectionlistener import ConnectionListener
from .queue import ConnectionEstablished, ConnectionLost, DataReceived
from .. import Packet

class UnknownItem(ValueError):
   def __init__(self, item):
      self.__item = item
   
   @property
   def item(self):
      return self.__item


class Port:
   def __init__(self, parser, portNotOpenException, PortExceptionType):
      self.__PortExceptionType = PortExceptionType
      self.__connectionListeners = set()
      self.__debugRead = False
      self.__debugWrite = False
      self.__errorProcessor = print
      self.__packet = None
      self.__parser = parser
      self.__portNotOpenException = portNotOpenException
      self.__queue = SimpleQueue()
   
   @property
   def debugRead(self):
      return self.__debugRead
   
   @debugRead.setter
   def debugRead(self, debugRead):
      self.__debugRead = debugRead
   
   @property
   def debugWrite(self):
      return self.__debugWrite
   
   @debugWrite.setter
   def debugWrite(self, debugWrite):
      self.__debugWrite = debugWrite
   
   @property
   def errorProcessor(self):
      return self.__errorProcessor
   
   @errorProcessor.setter
   def errorProcessor(self, errorProcessor):
      self.__errorProcessor = errorProcessor
   
   @property
   def parser(self):
      return self.__parser
   
   def addConnectionListener(self, connectionListener):
      self.__addRemoveConnectionListener(True, connectionListener)
   
   def addQueueItem(self, item):
      self.__queue.put_nowait(item)
   
   def close(self):
      if self.isOpen():
         self._close()
   
   def isOpen(self):
      StaticUtils.notImplemented()
   
   def open(self, path, **kw):
      try:
         self._open(path, **kw)
         
         return True
      
      except self.__PortExceptionType as e:
         self.errorProcessor(e)
   
   def packet(self, **kw):
      self.__packet = Packet(self.__parser.format, **kw)
      
      return self
   
   def removeConnectionListener(self, connectionListener):
      self.__addRemoveConnectionListener(False, connectionListener)
   
   def processQueue(self):
      try:
         item = self.__queue.get_nowait()
         
         if isinstance(item, ConnectionEstablished):
            for connectionListener in self.__connectionListeners:
               connectionListener.connectionEstablished(self)
         
         elif isinstance(item, ConnectionLost):
            for connectionListener in self.__connectionListeners:
               connectionListener.connectionLost(self, item.e)
         
         elif isinstance(item, DataReceived):
            self.__parser.parse(item.data)
         
         else:
            raise UnknownItem(item)
      
      except Empty:
         pass
   
   def write(self, packet = None, throw = False):
      if not packet:
         packet = self.__packet
      
      try:
         if self.__debugWrite:
            print(list(packet.rawBuffer))
         
         else:
            if not self.isOpen():
               raise self.__portNotOpenException
            
            self._write(packet)
         
         return True
      
      except self.__PortExceptionType as e:
         if throw:
            raise
         
         self.__errorProcessor(e)
      
      finally:
         self.__packet = None
   
   def _close(self):
      StaticUtils.notImplemented()
   
   def _open(self, path, **kw):
      StaticUtils.notImplemented()
   
   def _write(self, packet):
      StaticUtils.notImplemented()
   
   def __addRemoveConnectionListener(self, add, connectionListener):
      StaticUtils.assertInheritance(connectionListener, ConnectionListener, "connectionListener")
      
      getattr(self.__connectionListeners, "add" if add else "remove")(connectionListener)
