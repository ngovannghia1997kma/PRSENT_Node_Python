from dynamic_Sbox_pypresent import Present

key = "0123456789abcdef0123456789abcdef".decode('hex')
plain = "0123456789abcdef".decode('hex')
cipher = Present(key)
encrypted = cipher.encrypt(plain)
print(encrypted.encode('hex'))
# '0e9d28685e671dd6'
decrypted = cipher.decrypt(encrypted)
print(decrypted.encode('hex'))
# '0123456789abcdef'