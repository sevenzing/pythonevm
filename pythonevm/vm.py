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
        

def execute(code: bytearray, stack: Stack, memory: bytearray, storage: dict, msg: bytearray, toprint=False):
    '''
    :param code: e.g. b'\0x60\0x01\0x60\0x01\0x01'
    :param stack: Stack() instance
    :param memory: bytearray for memory
    :param storage: dict for storage
    :param msg: msg.data, call data values
    :param toprint: if true then it will print status after each instruction
    '''
    pc = 0

    while pc < code.__len__():
        # |60|03|60|04|01|
        #        /\
        #        ||
        #        pc = 0002

        opcode = code[pc]

        if opcode not in opcodes:
            raise KeyError(f"I can not find such opcode '{opcode}'. pc = {pc}")

        opcodename, in_args, out_args, fee = opcodes[opcode]

        if len(stack) < in_args:
            print(f"Error: stack has length {len(stack)} but {opcodename} (PC={pc}) has to have {in_args} input args.")
            return b""

        amountOfArgs = 0
        # -----------
        # 0x00 - 0x10
        # -----------

        if opcodename == "STOP":
            return b""
        elif opcodename == "ADD":
            a, b = stack.popTop(sign=True), stack.popTop(sign=True)
            stack.put(a + b)
        elif opcodename == "MUL":
            stack.put(stack.popTop(sign=True) * stack.popTop(sign=True))
        elif opcodename == "SUB":
            stack.put(stack.popTop(sign=True) - stack.popTop(sign=True))
        elif opcodename == "DIV":
            a, b = stack.popTop(), stack.popTop()
            stack.put(0 if b == 0 else a // b)
        elif opcodename == "SDIV":
            a, b = stack.popTop(sign=True), stack.popTop(sign=True)
            stack.put(0 if b == 0 else a // b)
        elif opcodename == "MOD":
            a, b = stack.popTop(), stack.popTop()
            stack.put(0 if b == 0 else a % b)
        elif opcodename == "SMOD":
            a, b = stack.popTop(sign=True), stack.popTop(sign=True)
            stack.put(0 if b == 0 else a % b)
        elif opcodename == "ADDMOD":
            a, b, N = stack.popTop(sign=True), \
                      stack.popTop(sign=True), \
                      stack.popTop(sign=True)
            stack.put(0 if N == 0 else (a + b) % N)
        elif opcodename == "MULMOD":
            a, b, N = stack.popTop(sign=True), \
                      stack.popTop(sign=True), \
                      stack.popTop(sign=True)
            stack.put(0 if N == 0 else (a * b) % N)
        elif opcodename == "EXP":
            stack.put(stack.popTop() ** stack.popTop())
        elif opcodename == "SIGNEXTEND":
            raise Exception("Opcode is not implemented yet")

        # -----------
        # 0x10 - 0x19
        # -----------

        elif opcodename == "LT":
            stack.put(1 if stack.popTop() < stack.popTop() else 0)
        elif opcodename == "GT":
            stack.put(1 if stack.popTop() > stack.popTop() else 0)
        elif opcodename == "SLT":
            a, b = stack.popTop(sign=True), stack.popTop(sign=True)
            stack.put(1 if a < b else 0)
        elif opcodename == "SGT":
            a, b = stack.popTop(sign=True), stack.popTop(sign=True)
            stack.put(1 if a > b else 0)
        elif opcodename == "EQ":
            stack.put(1 if stack.popTop() == stack.popTop() else 0)
        elif opcodename == "ISZERO":
            stack.put(1 if stack.popTop() == 0 else 0)
        elif opcodename == "AND":
            stack.put(stack.popTop() & stack.popTop())
        elif opcodename == "OR":
            stack.put(stack.popTop() | stack.popTop())
        elif opcodename == "XOR":
            stack.put(stack.popTop() ^ stack.popTop())
        elif opcodename == "NOT":
            stack.put(stack.popTop() ^ (2 ** stack.size - 1))

        # -----------
        # 0x1A - 0x1D
        # -----------

        elif opcodename == "BYTE":
            i, x = stack.popTop(), stack.popTop()
            # idk what is it
            stack.put((x >> (248 - i * 8)) & 0xFF)
        elif opcodename == "SHL":
            shift, value = stack.popTop(sign=True), stack.popTop(sign=True)
            stack.put(value << shift)
        elif opcodename == "SHR":
            shift, value = stack.popTop(sign=True), stack.popTop(sign=True)
            stack.put(value >> shift)
        elif opcodename == "SAR":
            shift, value = stack.popTop(), stack.popTop()
            stack.put(value >> shift)

        # --------
        #
        # --------

        elif opcodename == "CALLDATALOAD":
            offset = stack.popTop()

            if offset + 32 > len(msg):
                print(
                    f"Error: message data has length {len(msg)} "
                    f"but {opcodename} (PC={pc}) refers to [{offset}:{offset + 32}]")
                return b""
            value = msg[offset:offset + 32]
            stack.put(fromByteArrayToInt(value))
        elif opcodename == "CALLDATASIZE":
            stack.put(len(msg))
        elif opcodename == "CALLDATACOPY":
            destOffset, offset, length = stack.popTop(), stack.popTop(), stack.popTop()
            if destOffset + length > len(memory):
                print(
                    f"Error: memory has length {len(memory)} "
                    f"but {opcodename} (PC={pc}) refers to [{destOffset}:{destOffset + length}]")
                return b""
            if offset + length > len(msg):
                print(
                    f"Error: message data has length {len(msg)} "
                    f"but {opcodename} (PC={pc}) refers to [{offset}:{offset + length}]")
                return b""

            memory[destOffset:destOffset + length] = msg[offset:offset + length]

        # -----------
        # 0x50 - 0x58
        # -----------

        elif opcodename == "POP":
            stack.popTop()
        elif opcodename == "MLOAD":
            offset = stack.popTop()
            if offset + 32 > len(memory):
                stack.put(0)
            else:
                value = memory[offset:offset + 32]
                stack.put(fromByteToInt(value))
        elif opcodename == "MSTORE":
            offset = stack.popTop()
            value = stack.popTop()
            memory = extendMemory(memory, offset)
            memory[offset:offset + 32] = value.to_bytes(32, byteorder='big')
        elif opcodename == "MSTORE8":
            offset = stack.popTop()
            value = stack.popTop()
            memory = extendMemory(memory, offset)
            memory[offset:offset + 32] = (value & 0xFF).to_bytes(32, byteorder='big')
        elif opcodename == "SLOAD":
            key = stack.popTop(sign=True)
            if key in storage:
                value = storage[key]
            else:
                value = 0
            stack.put(value)
        elif opcodename == "SSTORE":
            key = stack.popTop(sign=True)
            value = stack.popTop(sign=True)
            storage[key] = value
        elif opcodename == "JUMP":
            destination = stack.popTop()
            if code[destination] not in opcodes:
                raise Exception(f"Destination {destination} not in opcodes")
            if code[destination] != 0x5b:
                print(f"Error: Destination has to be JUMPDEST [0x5B] but it is {code[destination]}. (PC={pc})")
                return b""
            pc = destination
        elif opcodename == "JUMPI":
            destination, condition = stack.popTop(), stack.popTop()
            if code[destination] not in opcodes:
                raise Exception(f"Destination {destination} not in opcodes")
            if code[destination] != 0x5b:
                print(f"Error: Destination has to be JUMPDEST [0x5B] but it is {code[destination]}. (PC={pc})")
                return b""
            pc = destination if condition else pc + 1
        elif opcodename == "JUMPDEST":
            pass
        elif opcodename == "PC":
            stack.put(pc)

        # -----------
        # 0x60 - 0x9F
        # -----------

        elif opcodename.startswith("PUSH"):
            amountOfArgs = int(opcodename.replace("PUSH", ""))
            value = fromByteToInt(code[pc + 1:pc + amountOfArgs + 1])
            stack.put(value)
            pc += amountOfArgs
        elif opcodename.startswith("DUP"):
            amountOfArgs = int(opcodename.replace("DUP", "")) - 1
            value = stack.getElement(amountOfArgs)
            stack.put(value)
            amountOfArgs = 0
        elif opcodename.startswith("SWAP"):
            amountOfArgs = int(opcodename.replace("SWAP", ""))
            value1, value2 = stack.getElement(0), stack.getElement(amountOfArgs)
            stack.setElement(0, value2)
            stack.setElement(amountOfArgs, value1)
            amountOfArgs = 0
        # -----------
        # 0xF3 - 0xF3
        # -----------

        elif opcodename == "RETURN":
            offset = stack.popTop()
            length = stack.popTop()
            return memory[offset:offset + length]

        else:
            raise Exception(f"We have not such opcode yet {opcodename}")

        if toprint:
            args = code[pc - amountOfArgs + 1:pc + 1].hex()
            args = [args[i:i + 2] for i in range(0, len(args), 2)]
            print(f"[ {str(pc - amountOfArgs).zfill(2)}: {opcodename}{' ' if len(args) != 0 else ''}{' '.join(args)} ] has executed.")

            stack.pprint()

            pprintMemory(memory)

            print(f"Storage: {storage}")
            print('-' * 10)

        # If opcode is JUMP or JUMPI instruction, then skip this step
        if not opcodename in ["JUMP", "JUMPI"]:
            pc += 1
