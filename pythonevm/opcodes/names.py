opcode_names = {
    0x00: 'STOP',
    0x01: 'ADD',
    0x02: 'MUL',
    0x03: 'SUB',
    0x04: 'DIV',
    0x05: 'SDIV',
    0x06: 'MOD',
    0x07: 'SMOD',
    0x08: 'ADDMOD',
    0x09: 'MULMOD',
    0x0a: 'EXP',
    0x0b: 'SIGNEXTEND',
    0x10: 'LT',
    0x11: 'GT',
    0x12: 'SLT',
    0x13: 'SGT',
    0x14: 'EQ',
    0x15: 'ISZERO',
    0x16: 'AND',
    0x17: 'OR',
    0x18: 'XOR',
    0x19: 'NOT',
    0x1a: 'BYTE',
    0x1b: 'SHL',
    0x1c: 'SHR',
    0x1d: 'SAR',
    0x35: 'CALLDATALOAD',
    0x36: 'CALLDATASIZE',
    0x37: 'CALLDATACOPY',
    0x3d: 'RETURNDATASIZE',
    0x3e: 'RETURNDATACOPY',
    0x50: 'POP',
    0x51: 'MLOAD',
    0x52: 'MSTORE',
    0x53: 'MSTORE8',
    0x54: 'SLOAD',
    0x55: 'SSTORE',
    0x56: 'JUMP',
    0x57: 'JUMPI',
    0x58: 'PC',
    0x59: 'MSIZE',
    0x5b: 'JUMPDEST',
    0xf3: 'RETURN',
    0xf5: 'CALLBLACKBOX',
    0xfa: 'STATICCALL',
    0xfd: 'REVERT',
    0xff: 'SUICIDE',
}


for i in range(1, 33):
    opcode_names[0x5f + i] = f'PUSH{i}'

for i in range(1, 17):
    opcode_names[0x7f + i] = f'DUP{i}'
    opcode_names[0x8f + i] = f'SWAP{i}'

