from dynamic_Sbox_pypresent import Present
import sys

argKey = str(sys.argv[2])
key = argKey.decode('hex')
argEncrypted = str(sys.argv[1])
encrypted = argEncrypted.decode('hex')
cipher = Present(key)
decrypted = cipher.decrypt(encrypted)
print(decrypted.encode('hex'))