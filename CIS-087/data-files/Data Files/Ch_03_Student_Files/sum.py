theSum = 0.0
data = input("Enter a number: ")
while data != "":
    number = float(data)
    theSum += number
    data = input("Enter the next number: ")
print("The sum is", theSum)
