#!/usr/bin/python3

import os

KEY_LENGTH = 256

global global_s

def KSA(key):
    keylength = len(key)

    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def PRGA(S):
    i = 0
    j = 0
    cnt = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        cnt += 1
        S[i], S[j] = S[j], S[i]
        
        global global_s
        global_s = S

        # K = S[(S[i] + S[j]) % 256] # vanilla RC4
        K = S[j] # Charlie's modification for uRC4
        yield K
        


def RC4(key):
    S = KSA(key)
    K = PRGA(S)

    return K


def encrypt(keystream, plaintext):
    ciphertext = [chr(ord(ch) ^ next(keystream)) for ch in list(plaintext)]

    # represent as hex string
    hex_ciphertext = ''.join("{:02X}".format(ord(ch)) for ch in ciphertext)

    return hex_ciphertext

def decrypt(keystream, ciphertext):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        plaintext += chr(int(ciphertext[i:i+2], 16) ^ next(keystream))
    return plaintext

if __name__ == '__main__':
    # Use a random 256-byte key to generate RC4 keystream
    key = [ord(os.urandom(1)) for i in range(KEY_LENGTH)]
    keystream = RC4(key)

    # The secret key `target` requires
    secret_key = "qwertyuioasdfghjk"

    banner = """=-=-=-=-=-=-= uRC4 encryption server -=-=-=-=-=-=-=
Welcome! uRC4 is an upgraded version of vanilla RC4
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="""
    print(banner)

    while True:
        menu = """
1. Encrypt your plaintext using uRC4 and print the ciphertext
2. Encrypt the secret key using uRC4 and print
3. Exit"""
        print(menu)

        choice = input(">>> ")
        if choice =='':
            continue

        choice = int(choice)

        if choice == 1:
            print("- Give me your plaintext:")
            plaintext = "\x00" * 0x1000
            exploit = (encrypt(keystream, plaintext))
            
            s_box =  [-1] * 256

            cnt = 0
            i = 0
            j = 0

            while(1):
                s_i = int(exploit[cnt * 2:cnt * 2 + 2], 16)
                
                i = (i + 1) % 256
                j = (j + s_i) % 256

                s_box[i], s_box[j] = s_box[j], s_i
                
                cnt += 1
                
                if cnt == 0x1000:
                    break
                    
            print(s_box)
            print(global_s)
            assert s_box == global_s
            
        elif choice == 2:
            print("- Encrypted secret key:")
            ciphertext = encrypt(keystream, secret_key)
            print(ciphertext)
            
            geted_keystream = PRGA(s_box)
            print(decrypt(geted_keystream, ciphertext))
            
            print("s_box: ", s_box)
            print("global_s: ", global_s)
            
            assert s_box == global_s
            
        else:
            print("- Bye")
            exit(0)
            