from opcodes import opcode_tag 
from pythonevm.numbers import fromByteToInt, fromByteArrayToInt

@opcode_tag(name='STOP')
def stop(vm):
    vm.stop = True

@opcode_tag(name='ADD')
def _add(vm):
    vm.stack.put(
        vm.stack.popTop(sign=True) + vm.stack.popTop(sign=True)
        )

@opcode_tag(name='MUL')
def _mul(vm):
    vm.stack.put(
        vm.stack.popTop(sign=True) * vm.stack.popTop(sign=True)
        )
@opcode_tag(name='SUB')
def _sub(vm):
    vm.stack.put(
        vm.stack.popTop(sign=True) - vm.stack.popTop(sign=True)
        )
@opcode_tag(name='DIV')
def _div(vm):
    a, b = vm.stack.popTop(), vm.stack.popTop()
    vm.stack.put(0 if b == 0 else a // b)

@opcode_tag(name='SDIV')
def _sdiv(vm):
    a, b = vm.stack.popTop(sign=True), vm.stack.popTop(sign=True)
    vm.stack.put(0 if b == 0 else a // b)

@opcode_tag(name='MOD')
def _mod(vm):
    a, b = vm.stack.popTop(), vm.stack.popTop()
    vm.stack.put(0 if b == 0 else a % b)

@opcode_tag(name='SMOD')
def _smod(vm):
    a, b = vm.stack.popTop(sign=True), vm.stack.popTop(sign=True)
    vm.stack.put(0 if b == 0 else a % b)

@opcode_tag(name='ADDMOD')
def _addmod(vm):
    a = vm.stack.popTop(sign=True)
    b = vm.stack.popTop(sign=True) 
    N = vm.stack.popTop(sign=True)
    vm.stack.put(0 if N == 0 else (a + b) % N)

@opcode_tag(name='MULMOD')
def _mul(vm):
    a = vm.stack.popTop(sign=True)
    b = vm.stack.popTop(sign=True) 
    N = vm.stack.popTop(sign=True)
    vm.stack.put(0 if N == 0 else (a * b) % N)

@opcode_tag(name='EXP')
def _exp(vm):
    # assume that stack contains only integer values
    vm.stack.put(vm.stack.popTop() ** vm.stack.popTop())

@opcode_tag(name='LT')
def _lt(vm):
    vm.stack.put(1 if vm.stack.popTop() < vm.stack.popTop() else 0)

@opcode_tag(name='GT')
def _gt(vm):
    vm.stack.put(1 if vm.stack.popTop() > vm.stack.popTop() else 0)

@opcode_tag(name='SLT')
def _slt(vm):
    a, b = vm.stack.popTop(sign=True), vm.stack.popTop(sign=True)
    vm.stack.put(1 if a < b else 0)

@opcode_tag(name='SGT')
def _sgt(vm):
    a, b = vm.stack.popTop(sign=True), vm.stack.popTop(sign=True)
    vm.stack.put(1 if a > b else 0)

@opcode_tag(name='EQ')
def _eq(vm):
    vm.stack.put(1 if vm.stack.popTop() == vm.stack.popTop() else 0)

@opcode_tag(name='ISZERO')
def _iszero(vm):
    vm.stack.put(1 if vm.stack.popTop() == 0 else 0)

@opcode_tag(name='AND')
def _and(vm):
    vm.stack.put(vm.stack.popTop() & vm.stack.popTop())

@opcode_tag(name='OR')
def _or(vm):
    vm.stack.put(vm.stack.popTop() | vm.stack.popTop())

@opcode_tag(name='XOR')
def _xor(vm):
    vm.stack.put(vm.stack.popTop() ^ vm.stack.popTop())

@opcode_tag(name='NOT')
def _not(vm):
    vm.stack.put(vm.stack.popTop() ^ (2 ** vm.stack.size - 1))

@opcode_tag(name='BYTE')
def _byte(vm):
    i, x = vm.stack.popTop(), vm.stack.popTop()
    vm.stack.put((x >> (248 - i * 8)) & 0xFF)

@opcode_tag(name='SHL')
def _shl(vm):
    shift, value = vm.stack.popTop(sign=True), vm.stack.popTop(sign=True)
    vm.stack.put(value << shift)

@opcode_tag(name='SHR')
def _shr(vm):
    shift, value = vm.stack.popTop(sign=True), vm.stack.popTop(sign=True)
    vm.stack.put(value >> shift)

@opcode_tag(name='SAR')
def _sar(vm):
    shift, value = vm.stack.popTop(), vm.stack.popTop()
    vm.stack.put(value >> shift)

@opcode_tag(name='CALLDATALOAD')
def _calldataload(vm):
    offset = vm.stack.popTop()

    if offset + 32 > len(vm.msg):
        raise Exception(
            f"Error: message data has length {len(vm.msg)} "
            f"but {vm.current_opcode_name} (PC={vm.pc}) refers to [{offset}:{offset + 32}]")
    
    value = vm.msg[offset:offset + 32]
    vm.stack.put(fromByteArrayToInt(value))

@opcode_tag(name='CALLDATASIZE')
def _calldatasize(vm):
    vm.stack.put(len(vm.msg))

@opcode_tag(name='CALLDATACOPY')
def _calldatacopy(vm):
    destOffset = vm.stack.popTop()
    offset = vm.stack.popTop()
    length = vm.stack.popTop()
    if destOffset + length > len(vm.memory):
        raise Exception(
            f"Error: memory has length {len(vm.memory)} "
            f"but {vm.opcodename} (PC={vm.pc}) refers to [{destOffset}:{destOffset + length}]")

    if offset + length > len(vm.msg):
        raise Exception(
            f"Error: message data has length {len(vm.msg)} "
            f"but {vm.current_opcode_name} (PC={vm.pc}) refers to [{offset}:{offset + length}]")

    memory[destOffset:destOffset + length] = vm.msg[offset:offset + length]


@opcode_tag(name='POP')
def _pop(vm):
    vm.stack.popTop()

@opcode_tag(name='MLOAD')
def _mload(vm):
    offset = vm.stack.popTop()
    if offset + 32 > len(vm.memory):
        vm.stack.put(0)
    else:
        value = vm.memory.get_raw()[offset:offset + 32]
        vm.stack.put(fromByteToInt(value))

@opcode_tag(name='MSTORE')
def _mstore(vm):
    offset = vm.stack.popTop()
    value = vm.stack.popTop()
    vm.memory.extend(offset)
    vm.memory.get_raw()[offset:offset + 32] = value.to_bytes(32, byteorder='big')

@opcode_tag(name='MSTORE8')
def _mstore8(vm):
    offset = vm.stack.popTop()
    value = vm.stack.popTop()
    vm.memory.extend(offset)
    vm.memory.get_raw()[offset:offset + 32] = (value & 0xFF).to_bytes(32, byteorder='big')
    

@opcode_tag(name='SLOAD')
def _sload(vm):
    key = vm.stack.popTop(sign=True)
    vm.stack.put(vm.storage.get(key, 0))

@opcode_tag(name='SSTORE')
def _sstore(vm):
    key = vm.stack.popTop(sign=True)
    value = vm.stack.popTop(sign=True)
    vm.storage[key] = value

@opcode_tag(name='JUMP')
def _jump(vm, destination=None):
    if destination == None:
        destination = vm.stack.popTop()
    if vm.code[destination] != 0x5b:
        raise Exception(f"Error: Destination has to be JUMPDEST[0x5b] but it is {vm.code[destination]} at {vm.pc}")
    vm.make_pc_move(jump_to=destination)

@opcode_tag(name='JUMPI')
def _jumpi(vm):
    destination, condition = vm.stack.popTop(), vm.stack.popTop()
    if condition:
        _jump(vm, destination)
    
@opcode_tag(name='JUMPDEST')
def _jumpdest(vm):
    pass

@opcode_tag(name='PC')
def _pc(vm):
    vm.stack.put(vm.pc)

@opcode_tag(name='RETURN')
def _return(vm):
    offset = vm.stack.popTop()
    length = vm.stack.popTop()
    vm.stop = True
    return vm.memory.get_raw()[offset:offset + length]

@opcode_tag(name=r'PUSH\d+')
def _push(vm):
    amountOfArgs = int(vm.current_opcode_name.replace("PUSH", ""))
    value = fromByteToInt(vm.code[vm.pc + 1:vm.pc + amountOfArgs + 1])
    vm.stack.put(value)
    vm.make_pc_move(amountOfArgs + 1)
    
@opcode_tag(name=r'DUP\d+')
def _dup(vm):
    amountOfArgs = int(vm.current_opcode_name.replace("DUP", "")) - 1
    value = vm.stack.getElement(amountOfArgs)
    vm.stack.put(value)

@opcode_tag(name=r'SWAP\d+')
def _swap(vm):
    amountOfArgs = int(vm.current_opcode_name.replace("SWAP", ""))
    value1, value2 = vm.stack.getElement(0), vm.stack.getElement(amountOfArgs)
    vm.stack.setElement(0, value2)
    vm.stack.setElement(amountOfArgs, value1)

