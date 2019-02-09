class Field:
   __formats = {
      1: ["B"],
      2: ["H"],
      4: ["L"],
      8: ["Q"]
   }
   
   [{value.append(value[0].lower()) for value in __formats.values()}]
   
   def __init__(self, size, signed = None, precedingField = None):
      self.__offset = 0 if precedingField == None else precedingField.nextOffset
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
   def nextOffset(self):
      return self.__offset + self.__size
   
   @property
   def value(self):
      return self.__value
   
   @value.setter
   def value(self, value):
      self.__value = value
   
   def __read(self, buf, offset, byteorder):
      pass
   
   def _write(self, buf, offset, byteorder):
      pass
