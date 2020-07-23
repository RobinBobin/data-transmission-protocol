class ConnectionLost:
   def __init__(self, e):
      self.__e = e
   
   @property
   def e(self):
      return self.__e
