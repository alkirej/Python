import os

inputFilename = input("Enter full path to file to be encrypted: ")

if True == os.path.exists(inputFilename):
    fileReader = open(inputFilename, 'r')

    decryptedText = fileReader.read()
    distance = 3

    lowerBound = '!'
    upperBound = '~'

    encrypted = ""

    for character in decryptedText:
        ordValue = ord(character)
        cipherValue = ordValue + distance

        if cipherValue > ord(upperBound):
            index1 = ord(lowerBound) + distance
            index2 = ord(upperBound) - ordValue + 1
            indexSum = index1 - index2
            cipherValue = indexSum
        
        encrypted += chr(cipherValue)

    print("Your file was encrypted: " + encrypted)
else:
    print("The file does not exist!")

inputFilename = input("Enter full path to file to be decrypted: ")

if True == os.path.exists(inputFilename):
    fileReader = open(inputFilename, 'r')

    encryptedText = fileReader.read()
    distance = 3

    lowerBound = '!'
    upperBound = '~'

    decrypted = ""

    for character in encryptedText:
        ordValue = ord(character)
        cipherValue = ordValue - distance

        if cipherValue < ord(lowerBound):
            index1 = ord(upperBound) - distance
            index2 = ord(lowerBound) - ordValue - 1
            indexSum = index1 - index2
            cipherValue = indexSum

        decrypted += chr(cipherValue)

    print("Your file was decrypted: " + decrypted)
else:
    print("The file does not exist!")