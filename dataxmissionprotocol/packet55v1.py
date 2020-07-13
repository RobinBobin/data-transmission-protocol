from .formats import Formats, zx55v1
from .packet import Packet

class Packet55v1(Packet):
   def __init__(self, **kwargs):
      super().__init__(Formats.zx55v1, **kwargs)
   
   @staticmethod
   def getFormat():
      return Formats.zx55v1
