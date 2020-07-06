# !/usr/bin/python
# -*- coding: utf-8 -*-

""" PRESENT block cipher implementation

USAGE EXAMPLE:
---------------
Importing:
-----------
>>> from pypresent import Present

Encrypting with a 80-bit key:
------------------------------
>>> key = "00000000000000000000".decode('hex')
>>> plain = "0000000000000000".decode('hex')
>>> cipher = Present(key)
>>> encrypted = cipher.encrypt(plain)
>>> encrypted.encode('hex')
'5579c1387b228445'
>>> decrypted = cipher.decrypt(encrypted)
>>> decrypted.encode('hex')
'0000000000000000'

Encrypting with a 128-bit key:
-------------------------------
>>> key = "0123456789abcdef0123456789abcdef".decode('hex')
>>> plain = "0123456789abcdef".decode('hex')
>>> cipher = Present(key)
>>> encrypted = cipher.encrypt(plain)
>>> encrypted.encode('hex')
'0e9d28685e671dd6'
>>> decrypted = cipher.decrypt(encrypted)
>>> decrypted.encode('hex')
'0123456789abcdef'

"""
class Present:

        def __init__(self,key,rounds=32):
                """Create a PRESENT cipher object

                key:    the key as a 128-bit or 80-bit rawstring
                rounds: the number of rounds as an integer, 32 by default
                """
                self.rounds = rounds
                if len(key) * 8 == 80:
                        self.roundkeys = generateRoundkeys80(string2number(key),self.rounds)
                elif len(key) * 8 == 128:
                        self.roundkeys = generateRoundkeys128(string2number(key),self.rounds)
                else:
                        raise ValueError, "Key must be a 128-bit or 80-bit rawstring"

        def encrypt(self,block):
                """Encrypt 1 block (8 bytes)

                Input:  plaintext block as raw string
                Output: ciphertext block as raw string
                """
                state = string2number(block)
                for i in xrange (self.rounds-1):
                        state = addRoundKey(state,self.roundkeys[i])

                        # Create dynamic Sbox
                        # Ở mỗi vòng lặp ta sẽ gọi hàm dynamic_sbox để sinh ra một Sbox mới
                        sbox_dynamic = dynamic_sbox(self.roundkeys[i],i,Sbox)
                        
                        # Sau khi đã sinh ra được Sbox mới chúng ta sẽ sử dụng để mã hóa
                        # trong hàm sBoxLayer
                        state = sBoxLayer(state, sbox_dynamic)
                        state = pLayer(state)
                        
                cipher = addRoundKey(state,self.roundkeys[-1])
                
                return number2string_N(cipher,8)

        def decrypt(self,block):
                """Decrypt 1 block (8 bytes)

                Input:  ciphertext block as raw string
                Output: plaintext block as raw string
                """
                state = string2number(block)
                for i in xrange (self.rounds-1, 0, -1):
                        state = addRoundKey(state,self.roundkeys[i])
                        state = pLayer_dec(state)

                        # create dynamic Sbox_inv
                        # Mình đã mã hóa ở vòng nào thì sẽ sử dụng đúng Ki và i ở đó để 
                        # sinh ra Sbox_inv tương ứng. Vì đã mã hóa bằng Sbox nào thì chỉ 
                        # có Sbox_inv của nó mới có thể giải mã được
                        sbox_dynamic_dec = dynamic_sbox_dec(self.roundkeys[i-1],i-1,Sbox)
                        

                        # Truyền Sbox_inv vừa tính được để đưa vào hàm sBoxLayer_dec giải mã
                        state = sBoxLayer_dec(state, sbox_dynamic_dec)
                decipher = addRoundKey(state,self.roundkeys[0])
                return number2string_N(decipher,8)

        def get_block_size(self):
                return 8

#        0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
Sbox= [0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2]
Sbox_inv = [Sbox.index(x) for x in xrange(16)]
PBox = [0,16,32,48,1,17,33,49,2,18,34,50,3,19,35,51,
        4,20,36,52,5,21,37,53,6,22,38,54,7,23,39,55,
        8,24,40,56,9,25,41,57,10,26,42,58,11,27,43,59,
        12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
PBox_inv = [PBox.index(x) for x in xrange(64)]

############################################################################################################
######################## Phần cải tiến chuyển PRESNT từ Sbox tĩnh sang Sbox động ###########################
def dynamic_sbox(ki,i,sbox1):
        sbox = [i for i in sbox1]
        """Create dynamic Sbox

        Input: 
                Ki: is round key
                i: is round number
                Sbox: is Original Sbox 

        Output: array is Sbox new
        """
        # Position Ki
        pKi = ki % 16
        # Position i
        pI = i%16

        # Đổi chỗ của 2 vị trí mà ta đã tính ra từ Ki và i theo công thức (Ki mod 16) và (i mod 16)
        # với Ki là khóa vòng tại vòng lặp thứ i
        sbox[pKi], sbox[pI] = sbox[pI], sbox[pKi]

        return sbox

def dynamic_sbox_dec(ki,i,sbox1):
        sbox = [i for i in sbox1]

        """Create dynamic Sbox_dec

        Input: 
                Ki: is round key
                i: is round number
                sbox: is Original sbox 

        Output: array is Sbox_inv new
        """
        # Position Ki
        pKi = ki % 16
        # Position i
        pI = i%16

        # Tương tự sau khi đổi chỗ xong ta sẽ được 1 Sbox mới -> từ Sbox này ra sẽ sinh ra Sbox_inv
        sbox[pKi], sbox[pI] = sbox[pI], sbox[pKi]
        # Đây chính là phần sinh ra Sbox_inv:
        sbox_inv = [sbox.index(x) for x in xrange(16)]
        return sbox_inv

# Trên đây là 2 hàm để sinh Sbox mới và tạo ra Sbox_inv
############################################################################################################



def generateRoundkeys80(key,rounds):
        """Generate the roundkeys for a 80-bit key

        Input:
                key:    the key as a 80-bit integer
                rounds: the number of rounds as an integer
        Output: list of 64-bit roundkeys as integers"""
        roundkeys = []
        for i in xrange(1,rounds+1): # (K1 ... K32)
                # rawkey: used in comments to show what happens at bitlevel
                # rawKey[0:64]
                roundkeys.append(key >>16)
                #1. Shift
                #rawKey[19:len(rawKey)]+rawKey[0:19]
                key = ((key & (2**19-1)) << 61) + (key >> 19)
                #2. SBox
                #rawKey[76:80] = S(rawKey[76:80])
                key = (Sbox[key >> 76] << 76)+(key & (2**76-1))
                #3. Salt
                #rawKey[15:20] ^ i
                key ^= i << 15
        return roundkeys

def generateRoundkeys128(key,rounds):
        """Generate the roundkeys for a 128-bit key

        Input:
                key:    the key as a 128-bit integer
                rounds: the number of rounds as an integer
        Output: list of 64-bit roundkeys as integers"""
        roundkeys = []
        for i in xrange(1,rounds+1): # (K1 ... K32)
                # rawkey: used in comments to show what happens at bitlevel
                roundkeys.append(key >>64)
                #1. Shift
                key = ((key & (2**67-1)) << 61) + (key >> 67)
                #2. SBox
                key = (Sbox[key >> 124] << 124)+(Sbox[(key >> 120) & 0xF] << 120)+(key & (2**120-1))
                #3. Salt
                #rawKey[62:67] ^ i
                key ^= i << 62
        return roundkeys

def addRoundKey(state,roundkey):
        return state ^ roundkey

def sBoxLayer(state, sbox_dynamic):
        """SBox function for encryption

        Input:  64-bit integer
        Output: 64-bit integer"""

        output = 0
        for i in xrange(16):
                output += sbox_dynamic[( state >> (i*4)) & 0xF] << (i*4)
        return output

def sBoxLayer_dec(state, sbox_dynamic_dec):
        """Inverse SBox function for decryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in xrange(16):
                output += sbox_dynamic_dec[( state >> (i*4)) & 0xF] << (i*4)
        return output

def pLayer(state):
        """Permutation layer for encryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in xrange(64):
                output += ((state >> i) & 0x01) << PBox[i]
        return output

def pLayer_dec(state):
        """Permutation layer for decryption

        Input:  64-bit integer
        Output: 64-bit integer"""
        output = 0
        for i in xrange(64):
                output += ((state >> i) & 0x01) << PBox_inv[i]
        return output

def string2number(i):
    """ Convert a string to a number

    Input: string (big-endian)
    Output: long or integer
    """
    return int(i.encode('hex'),16)

def number2string_N(i, N):
    """Convert a number to a string of fixed size

    i: long or integer
    N: length of string
    Output: string (big-endian)
    """
    s = '%0*x' % (N*2, i)
    return s.decode('hex')

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
