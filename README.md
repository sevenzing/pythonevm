Python Ethereum Virtual Machine
===

### 1. What is that?
Todo
### 2. How to use it?
Todo
### 3. Testing
Test using framework `pytest`:

    $ python3 -m pip install pytest
    $ python3 -m pytest

### 4. Example
#### One plus two

```python3
from pythonevm.vm import VM
vm = VM()

# put 2 on the stack, 
# put 1 on the stack, 
# sum 2 numbers from the stack, 
# stop vm
bytecode = '600260010100'
code = bytearray(bytes.fromhex(bytecode))
msg = bytearray()

vm.execute(code, msg, debug=True)
```
