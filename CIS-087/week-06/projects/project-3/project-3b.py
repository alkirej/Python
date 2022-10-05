


LOWEST_CHAR_TO_ENCRYPT = ord(' ')
LARGEST_CHAR_TO_ENCRYPT = ord('~')

file_name = input("File to decrypt: ")
cipher_delta_str = input("Cipher distance: ")
cipher_delta = int(cipher_delta_str)

fd = open(file_name,'r')
contents = fd.read()
fd.close()

# Caesar Cipher loop
decrypted_str = ""
for ch in contents:
    n = ord(ch)
    # Encryptor passed out of range chars through, so we will to.
    if n>=LOWEST_CHAR_TO_ENCRYPT and n<=LARGEST_CHAR_TO_ENCRYPT:
        # encryption happens here.
        n -= cipher_delta
        if n < LOWEST_CHAR_TO_ENCRYPT:
            n = LARGEST_CHAR_TO_ENCRYPT - (LOWEST_CHAR_TO_ENCRYPT-n-1)

    # result string built here
    decrypted_str += chr(n)

fd = open(file_name+".dec",'w')
fd.write(decrypted_str)
fd.close()
