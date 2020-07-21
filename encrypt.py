from dynamic_Sbox_pypresent import Present
import sys

argKey = str(sys.argv[2])
key = argKey.decode('hex')
argPlain = str(sys.argv[1])
plain = argPlain.decode('hex')
cipher = Present(key)
encrypted = cipher.encrypt(plain)
print(encrypted)