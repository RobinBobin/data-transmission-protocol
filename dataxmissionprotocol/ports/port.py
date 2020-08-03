from commonutils import StaticUtils
from queue import Empty, SimpleQueue
from .connectionlistener import ConnectionListener
from .queue import ConnectionEstablished, ConnectionLost, DataReceived, ProcessError
from .. import Packet

class UnknownItem(ValueError):
   def __init__(self, item):
      self.__item = item
   
   @property
   def item(self):
      return self.__item


class Port:
   def __init__(self, parser, portNotOpenException, PortExceptionType = None):
      self.__PortExceptionType = PortExceptionType or type(portNotOpenException)
      self.__autoOpenOnWrite = False
      self.__connectionListeners = set()
      self.__debugRead = False
      self.__debugWrite = False
      self.__errorProcessor = print
      self.__packet = None
      self.__parser = parser
      self.__path = None
      self.__portNotOpenException = portNotOpenException
      self.__queue = SimpleQueue()
      self.__throw = False
   
   @property
   def autoOpenOnWrite(self):
      return self.__autoOpenOnWrite
   
   @autoOpenOnWrite.setter
   def autoOpenOnWrite(self, autoOpenOnWrite):
      self.__autoOpenOnWrite = autoOpenOnWrite
   
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
   
   @property
   def path(self):
      return self.__path
   
   @path.setter
   def path(self, path):
      self.__path = path
   
   @property
   def throw(self):
      return self.__throw
   
   @throw.setter
   def throw(self, throw):
      self.__throw = throw
   
   def Packet(self, **kw):
      return Packet(self.__parser.format, **kw)
   
   def addConnectionListener(self, connectionListener):
      self.__addRemoveConnectionListener(True, connectionListener)
   
   def addQueueItem(self, item):
      self.__queue.put_nowait(item)
   
   def close(self):
      if self.isOpen():
         self._close()
   
   def isOpen(self):
      StaticUtils.notImplemented()
   
   def open(self, path = None, **kw):
      try:
         self._open(path, **kw)
         
         return True
      
      except self.__PortExceptionType as e:
         self._processError(e)
      
      finally:
         self.__throw = False
   
   def packet(self, **kw):
      self.__packet = self.Packet(**kw)
      
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
         
         elif isinstance(item, ProcessError):
            self.__errorProcessor(item.e)
         
         else:
            raise UnknownItem(item)
      
      except Empty:
         pass
   
   def write(self, packet = None, throw = None):
      if not packet:
         packet = self.__packet
      
      if throw is not None:
         self.__throw = throw
      
      try:
         if self.__debugWrite:
            print(packet)
         
         else:
            if not self.isOpen():
               if self.__autoOpenOnWrite:
                  self._open()
               
               else:
                  raise self.__portNotOpenException
            
            self._write(packet)
         
         return True
      
      except self.__PortExceptionType as e:
         self._processError(e)
      
      finally:
         self.__packet = None
         self.__throw = False
   
   def _close(self):
      StaticUtils.notImplemented()
   
   def _open(self, path = None, **kw):
      StaticUtils.notImplemented()
   
   def _processError(self, e):
      if self.__throw:
         raise e
      
      if self.__errorProcessor:
         self.addQueueItem(ProcessError(e))
   
   def _write(self, packet):
      StaticUtils.notImplemented()
   
   def __addRemoveConnectionListener(self, add, connectionListener):
      StaticUtils.assertInheritance(connectionListener, ConnectionListener, "connectionListener")
      
      getattr(self.__connectionListeners, "add" if add else "remove")(connectionListener)
