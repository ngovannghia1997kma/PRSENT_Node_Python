from pypresent import Present
import sys


key = "00000000000000000000".decode('hex')
arg = str(sys.argv[1])
plain = arg.decode('hex')
cipher = Present(key)
encrypted = cipher.encrypt(plain)
print('Encrypted: '+ encrypted.encode('hex'))


