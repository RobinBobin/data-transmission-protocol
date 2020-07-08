from commonutils import StaticUtils
from struct import pack_into, unpack_from

class Field:
   __formats = {
      1: ["B"],
      2: ["H"],
      4: ["L"],
      8: ["Q"]
   }
   
   for v in __formats.values():
      v.append(v[0].lower())
   
   def __init__(self, size, **kwargs):
      previousField = kwargs.get("previousField")
      signed = kwargs.get("signed")
      
      self._offset = previousField.nextOffset if previousField else 0
      self.__size = size
      self.__format = None if signed == None else Field.__formats[size][+signed]
      self.__value = kwargs.get("value")
   
   @property
   def size(self):
      return self.__size
   
   @property
   def nextOffset(self):
      return self._offset + self.__size
   
   @property
   def value(self):
      return self.__value
   
   @value.setter
   def value(self, value):
      if self.__format != None:
         self.__value = value
      
      elif len(value) != self.__size:
         raise ValueError()
      
      else:
         self.__value = value[:]
   
   @staticmethod
   def createChain(size, signed = None, value = None):
      chain = []
      args = (size, signed, value)
      
      def count():
         for x in args:
            if StaticUtils.isIterable(x):
               return len(x)
         
         raise ValueError()
      
      for index in range(count()):
         params = tuple(v[index] if StaticUtils.isIterable(v) else v for v in args)
         
         chain.append(Field(
            params[0],
            previousField = chain[index - 1] if index else None,
            signed = params[1],
            value = params[2]))
      
      return chain
   
   def _get(self, buf, offset, byteorder):
      i = offset + self._offset
      j = i + self.__size
      
      self.__value = buf[i:j] if self.__format == None else unpack_from(f"{byteorder}{self.__format}", buf, i)[0]
      
      return self
   
   def _set(self, buf, offset, byteorder):
      i = offset + self._offset
      j = i + self.__size
      
      if self.__format == None:
         buf[i:j] = self.__value
      
      else:
         pack_into(f"{byteorder}{self.__format}", buf, i, self.__value)
