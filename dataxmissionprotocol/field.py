class Field:
   __formats = {
      1: ["B"],
      2: ["H"],
      4: ["L"],
      8: ["Q"]
   }
   
   [{value.append(value[0].lower()) for value in __formats.values()}]
   
   def __init__(self, size, signed = None):
      self.__offset = 0
      self.__size = size
      self.__format = None if signed == None else Field.__formats[size][+signed]
      self.__value = None
   
   @property
   def offset(self):
      return self.__offset
   
   @offset.setter
   def offset(self, offset):
      self.__offset = offset
   
   @property
   def size(self):
      return self.__size
   
   @property
   def value(self):
      return self.__value
   
   @value.setter
   def value(self, value):
      self.__value = value
