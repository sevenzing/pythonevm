IMPLEMENTED_OPCODES = {}


def opcode_tag(name):
    assert name not in IMPLEMENTED_OPCODES

    def decorator(function):

        def wrapper(VM, *args, **kwargs):
            try:
                result = function(VM, *args, **kwargs)
            except IndexError as e:
                raise IndexError(f"pop from empty stack while {VM}")
            except Exception as e:
                raise Exception(f'Error at {function.__name__}: {e}')
            return result

        IMPLEMENTED_OPCODES[name] = wrapper
        return wrapper
    return decorator



