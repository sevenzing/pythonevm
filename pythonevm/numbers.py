def safe_ord(value):
    if isinstance(value, int):
        return value
    else:
        return ord(value)


def signInt(integer, limit):
    a = 2 ** limit
    return integer if integer < a else integer - a


def toTwosComplement(value, bits):
    # If value < 0 then inverse bits and add 1
    if value < 0:
        value = 2 ** bits + value

    # Apply the mask 0xFFFF...FF
    return value & (2 ** bits - 1)


def fromTwosComplement(value: int, bits: int):
    if value > 2 ** (bits - 1) - 1:
        return -(2 ** bits - value)
    return value


def fromByteToInt(value: bytes):
    return int(value.hex(), 16)

    
def fromByteArrayToInt(barray: bytearray):
    return int(barray.hex(), 16)