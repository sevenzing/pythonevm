from opcodes.names import opcode_names
import opcodes.implementation 

from opcodes import IMPLEMENTED_OPCODES
from utils import Stack, Memory, OpcodeNotImplemented, OpcodeNotFound

import re


class VM:
    def __init__(self, stack_size=256, *args, **kwargs):
        self.stack = Stack(size=stack_size)
        self.memory = Memory(memory=kwargs.get('memory', b''))
        self.storage = dict()

        self.args = args
        self.kwargs = kwargs
        
        self.opcode = None
        self.current_opcode_name = None
        self.code = None
        self.msg = None
        self.code = None
        
        self.pc = 0
        self.prev_pc = -1
        self.stop = False
        
    def __str__(self, executed=False):
        if executed:
            _str = str(self.stack) + '\n' + str(self.memory)
        else:
            number = '0x' + hex(self.opcode)[2:].zfill(2)
            _str = f"Executing {self.current_opcode_name}[{number}] at position {self.pc}"
        return  _str
    
    def make_pc_move(self, shift=None, jump_to=None):
        if jump_to != None:
            self.prev_pc = self.pc
            self.pc = jump_to
            self.pc_moved = True

        elif shift != None and not self.pc_moved:
            self.prev_pc = self.pc
            self.pc += shift
            self.pc_moved = True

        else:
           pass

    def execute(self, code: bytearray, msg: bytearray, debug=False):
        '''
        Executes string of opcodes
        
        :param code: bytearray of opcodes: b'\x60\x01'
        :param msg: message bytearray. Usually stands for function call description  
        :param debug: if true, vm will log actions
        :retrun: result of RETURN opcode or None
        '''
        self.code = code
        self.msg = msg

        while not self.stop:
            self.pc_moved = False

            try:
                self.opcode = code[self.pc]
            except IndexError:
                raise EOFError(f'End of opcode string while {self}')

            if self.opcode not in opcode_names:
                raise OpcodeNotFound(f"Opcode {self.opcode} at program pointer {self.pc} wasn't found")
            
            self.current_opcode_name = opcode_names[self.opcode]
            
            print(self.__str__())
            # running opcode
            result = self.execute_opcode(self.current_opcode_name)
            if result:
                return result

            print(self.__str__(executed=True), end='\n\n')
            # pc move
            self.make_pc_move(shift=1)            
            
    def execute_opcode(self, opcode_name):
        try:
            for current_opcode_name in IMPLEMENTED_OPCODES:
                if re.match(f"^{current_opcode_name}$", opcode_name):
                    return IMPLEMENTED_OPCODES[current_opcode_name](self)
            raise KeyError
        except KeyError:
            raise NotImplementedError(f'Opcode {opcode_name} at position {self.pc} not implemented yet')
