from math import log

guess_count = 0
smallest = int(input("Enter the smallest guessable number: "))
biggest  = int(input("Enter the largest guessable number:  "))

guess_within = int( log( (biggest-smallest+1), 2 ) + 1 )
print()
print( "  I WILL GUESS YOUR NUMBER WITHIN %d guesses" % guess_within  )
print()
computer_guess = smallest + (biggest - smallest ) // 2

while True:
    guess_count += 1
    print()
    print( "My guess is: %4d" % computer_guess )
    print( "    Is your number:" )
    print( "         (B)igger than my guess," )
    print( "         (C)orrect, or")
    correct = (input ( "         (S)maller than my guess? "))[0]

    if "C" == correct or "c" == correct:
        print()
        print( " *** *** **************** *** ***" )
        print( " ***     I'M THE GREATEST     ***" )
        print( " ***   Got it in %2d guesses   *** " % guess_count )
        if guess_count <= guess_within:
            print( " ***     TOLD YOU I COULD     ***")
        else:
            print( " ***  Guess I couldn't do it  ***")
        print( " *** *** **************** *** ***" )
        break

    elif "B" == correct or "b" == correct:
        # guess a bigger #
        smallest       = computer_guess
        computer_guess = smallest + (biggest - smallest + 1 ) // 2

    elif "S" == correct or "s" == correct:
        # guess a smaller #
        biggest       = computer_guess
        computer_guess = biggest - (biggest - smallest + 1 ) // 2
    else:
        print()
        print("   INVALID OPTION, TRY AGAIN.")
