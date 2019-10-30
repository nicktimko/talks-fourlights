import ctypes

offset = 24
ctypes.c_char.from_address(id(4) + offset).value = 5

print("I see...")
