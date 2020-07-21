from dynamic_Sbox_pypresent import Present

print("----------key 80 bit---------")
key = "00000000000000000000".decode('hex')
plain = "0000000000000000".decode('hex')
cipher = Present(key)
encrypted = cipher.encrypt(plain)
print(encrypted.encode('hex'))
# '5579c1387b228445'
decrypted = cipher.decrypt(encrypted)
print(decrypted.encode('hex'))
# '0000000000000000'


print("----------key 128 bit---------")
key = "0123456789abcdef0123456789abcdef".decode('hex')
plain = "0123456789abcdef".decode('hex')
cipher = Present(key)
encrypted = cipher.encrypt(plain)
print(encrypted.encode('hex'))
# '0e9d28685e671dd6'
decrypted = cipher.decrypt(encrypted)
print(decrypted.encode('hex'))
# '0123456789abcdef'