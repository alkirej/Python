
LOWEST_CHAR_TO_ENCRYPT = ord(' ')
LARGEST_CHAR_TO_ENCRYPT = ord('~')

encrypt_me = input("Text to encrypt: ")
cipher_delta_str = input("Cipher distance: ")
cipher_delta = int(cipher_delta_str)

# Caesar Cipher loop
encrypted_str = ""
for ch in encrypt_me:
    n = ord(ch)
    n += cipher_delta

    if n > LARGEST_CHAR_TO_ENCRYPT:
        n = (n-LARGEST_CHAR_TO_ENCRYPT-1) + LOWEST_CHAR_TO_ENCRYPT

    encrypted_str += chr(n)

print()
print(encrypted_str)