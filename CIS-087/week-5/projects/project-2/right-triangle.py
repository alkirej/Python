PROMPT = "Please enter the length of side "
ANSWER_PREFIX = "This is "
ANSWER_SUFFIX = "a right triangle."

side_1 = input(PROMPT + "1: ")
len_1  = int( side_1 )
side_2 = input(PROMPT + "2: ")
len_2  = int( side_2 )
side_3 = input(PROMPT + "3: ")
len_3  = int( side_3 )

# find longest side
if ( len_1 >= len_2 and len_1 >= len_3 ):
    (a,b,c) = (len_2, len_3, len_1)
elif ( len_2 > len_3 ):
    (a,b,c) = (len_1, len_3, len_2)
else:
    (a,b,c) = (len_1, len_2, len_3)

if (a**2 + b**2 == c**2):
    answer = ""
else:
    answer = "NOT "

print()
print( ANSWER_PREFIX + answer + ANSWER_SUFFIX )
