
LOWEST_CHAR_TO_ENCRYPT = ord(' ')
LARGEST_CHAR_TO_ENCRYPT = ord('~')

encrypt_me = input("Text to decrypt: ")
cipher_delta_str = input("Cipher distance: ")
cipher_delta = int(cipher_delta_str)

# Caesar Cipher loop
decrypted_str = ""
for ch in encrypt_me:
    n = ord(ch)
    n -= cipher_delta

    if n < LOWEST_CHAR_TO_ENCRYPT:
        n = LARGEST_CHAR_TO_ENCRYPT - (LOWEST_CHAR_TO_ENCRYPT-n-1)
    decrypted_str += chr(n)

print()
print(decrypted_str)
