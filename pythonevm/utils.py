
from math import ceil
from pythonevm.numbers import *

def printError(message):
    print(f"Error: {message}")
    exit()


class Stack:
    def __init__(self, size=256):

        self.size = size
        self.__stk = []

    def put(self, value: int, index=0):
        """
        In stack all values are uint256.
        To store negative value I use
        toTwosComplement() function
        """
        if len(self.__stk) > 1024:
            raise Exception('Stack has lenght 1024')
        value = toTwosComplement(value, self.size)
        self.__stk.insert(index, value)

    def popTop(self, sign=False):
        """
        since stack contains only unsign values,
        to get sign value set sign-flag true
        """

        if not self.__stk.__len__():
            raise IndexError('pop from empty stack')

        if sign:
            return fromTwosComplement(self.__stk.pop(0), self.size)
        else:
            return self.__stk.pop(0)

    #
    # The same functions, but without add/remove and with indexes
    #

    def setElement(self, index, value):
        value = toTwosComplement(value, self.size)
        self.__stk[index] = value

    def getElement(self, index, sign=False):
        return None if index >= self.__stk.__len__() \
            else fromTwosComplement(self.__stk[index], self.size) \
            if sign else self.__stk[index]

    def __str__(self):
        messageToPrint = f'Stack [{len(self.__stk)}] : '

        for value in self.__stk:
            if str(value).__len__() > 20:
                messageToPrint += f"| {hex(value)[:10]}..{hex(value)[-10:]} "
            else:
                messageToPrint += f"| {hex(value)} "
        if self.__stk.__len__() == 0:
            messageToPrint += "| EMPTY STACK "
        messageToPrint += "|"

        return messageToPrint

    def __len__(self):
        return self.__stk.__len__()


class Memory:
    def __init__(self, memory=b''):
        _bytes = bytes()
        
        if isinstance(memory, int):
            amount_of_bytes = ceil((memory)/2**8)
            _bytes = memory.to_bytes(amount_of_bytes, byteorder='big')

        elif isinstance(memory, str):
            _bytes = bytes.fromhex(memory)
        
        else:
            try:
                _bytes = bytes(memory)
            except TypeError:
                raise TypeError('memory variable should be int, string or bytes')
        
        self.__mem = bytearray(_bytes)
    
    def __len__(self):
        return self.__mem.__len__()

    def extend(self, toIndex):
        to_extend = toIndex - len(self)
        self.__mem.extend(b'\x00' * to_extend)
        return len(self)

    def get_raw(self):
        return self.__mem

    def __str__(self):
        show_length = 20
        memoryHex = self.__mem.hex()
        if memoryHex.__len__() > show_length:
            memoryHex = f"{memoryHex[:(show_length//2)]}...{memoryHex[-(show_length//2):]}"
        
        return (f"Memory (0x{memoryHex})")



class OpcodeNotImplemented(Exception):
    def __init__(self, message):
        super(OpcodeNotImplemented, self).__init__(message)

class OpcodeNotFound(Exception):
    def __init__(self, message):
        super(OpcodeNotImplemented, self).__init__(message)

