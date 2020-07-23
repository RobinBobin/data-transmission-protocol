from commonutils import StaticUtils
from queue import Empty, SimpleQueue
from .connectionlistener import ConnectionListener
from .queue import ConnectionEstablished, ConnectionLost, DataReceived

class UnknownItem(ValueError):
   def __init__(self, item):
      self.__item = item
   
   @property
   def item(self):
      return self.__item


class Port:
   def __init__(self, parser):
      self.__connectionListeners = set()
      self.__debugRead = False
      self.__debugWrite = False
      self.__errorProcessor = print
      self.__parser = parser
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
   
   def __addRemoveConnectionListener(self, add, connectionListener):
      StaticUtils.assertInheritance(connectionListener, ConnectionListener, "connectionListener")
      
      getattr(self.__connectionListeners, "add" if add else "remove")(connectionListener)
