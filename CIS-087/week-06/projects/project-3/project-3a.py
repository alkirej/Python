


LOWEST_CHAR_TO_ENCRYPT = ord(' ')
LARGEST_CHAR_TO_ENCRYPT = ord('~')

file_name = input("File to encrypt: ")
cipher_delta_str = input("Cipher distance: ")
cipher_delta = int(cipher_delta_str)

fd = open(file_name,'r')
contents = fd.read()
fd.close()

# Caesar Cipher loop
encrypted_str = ""
for ch in contents:
    n = ord(ch)
    # Let's ignore characters outside of our boundaries and just pass them
    #       through.  Not a real world solution, but instructive here.
    if n>=LOWEST_CHAR_TO_ENCRYPT and n<=LARGEST_CHAR_TO_ENCRYPT:
        # encryption happens here.
        n += cipher_delta

        if n > LARGEST_CHAR_TO_ENCRYPT:
            n = (n-LARGEST_CHAR_TO_ENCRYPT-1) + LOWEST_CHAR_TO_ENCRYPT

    # result string built here
    encrypted_str += chr(n)

fd = open(file_name+".enc",'w')
fd.write(encrypted_str)
fd.close()