from commonutils import StaticUtils
from struct import calcsize, pack_into, unpack_from

class Field:
   __encoding = "utf-8"
   
   __formats = {
      1: ["B"],
      2: ["H"],
      3: ["L1"],
      4: ["L"],
      5: ["Q3"],
      6: ["Q2"],
      7: ["Q1"],
      8: ["Q"]
   }
   
   for v in __formats.values():
      v.append(v[0].lower())
   
   def __init__(self, size = None, **kw):
      previousField = kw.get("previousField")
      signed = kw.get("signed")
      value = kw.get("value")
      valueIsStr = not size
      
      self.__offset = previousField.nextOffset if previousField else 0
      self.__size = len(value) if valueIsStr else size
      
      self.__format = f"{self.__size}s" if valueIsStr else None if signed == None else Field.__formats[self.__size][+signed]
      
      self.__value = value.encode(Field.__encoding) if valueIsStr else value
   
   @property
   def nextOffset(self):
      return self.__offset + self.__size
   
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
      if self.__format != None:
         self.__value = value
      
      elif len(value) != self.__size:
         raise ValueError()
      
      else:
         self.__value = value[:]
   
   @staticmethod
   def createChain(size = None, signed = None, value = None, fields = None):
      chain = fields
      
      if chain:
         for i, field in enumerate(chain):
            if i:
               field.__offset = chain[i - 1].nextOffset
      
      else:
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
   
   @staticmethod
   def setEncoding(encoding):
      Field.__encoding = encoding
   
   def _get(self, buf, offset, byteorder):
      i = offset + self.__offset
      j = i + self.__size
      
      if self.__format == None:
         self.__value = buf[i:j]
      
      else:
         isStr = self.__format[0].isdigit()
         
         if len(self.__format) != 2 or isStr:
            self.__value = unpack_from(f"{byteorder}{self.__format}", buf, i)[0]
            
            if isStr:
               self.__value = self.__value.decode(Field.__encoding)
         
         else:
            self.__value = buf[i:j]
            
            for _ in range(int(self.__format[1])):
               if byteorder == ">":
                  self.__value[:0] = [0]
               
               else:
                  self.__value.append(0)
            
            self.__value = unpack_from(f"{byteorder}{self.__format[0]}", self.__value, 0)[0]
      
      return self
   
   def _set(self, buf, offset, byteorder):
      i = offset + self.__offset
      j = i + self.__size
      
      if self.__format == None:
         buf[i:j] = self.__value
      
      elif len(self.__format) != 2 or self.__format[0].isdigit():
         pack_into(f"{byteorder}{self.__format}", buf, i, self.__value)
      
      else:
         fmt = f"{byteorder}{self.__format[0]}"
         tmpbuf = bytearray(calcsize(fmt))
         
         pack_into(fmt, tmpbuf, 0, self.__value)
         
         for _ in range(int(self.__format[1])):
            tmpbuf.pop(0 if byteorder == ">" else -1)
         
         buf[i:j] = tmpbuf


class UnsignedField1(Field):
   def __init__(self, size = None, **kw):
      super().__init__(size = 1, signed = False, **kw)
