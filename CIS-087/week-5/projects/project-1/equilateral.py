PROMPT = "Please enter the length of side "
ANSWER_PREFIX = "This is "
ANSWER_SUFFIX = "an equilateral triangle."

side_1 = input(PROMPT + "1: ")
side_2 = input(PROMPT + "2: ")
side_3 = input(PROMPT + "3: ")

if (side_1 == side_2 == side_3):
    answer = ""
else:
    answer = "NOT "

print()
print( ANSWER_PREFIX + answer + ANSWER_SUFFIX )