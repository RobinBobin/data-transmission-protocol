class DataReceived:
   def __init__(self, data):
      self.__data = data
   
   @property
   def data(self):
      return self.__data
