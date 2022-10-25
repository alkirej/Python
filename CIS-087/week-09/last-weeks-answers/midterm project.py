import random

#Below is the loop and if else statements that define the first possibility of the game
for x in range(1):
    beginning = random.randint(1,4)
    outcome = beginning #outcome has to be defined due to beginning changing its value
if beginning == 1:
    beginning = "cave entrance, deep, dark and swarming with possibility."
    onechoice1 = "Arm yourself with a weapon!"
    onechoice2 = "Cower back and run away."
    onechoice3 = "Charge in with no fear!"
    onechoice4 = "Light a torch and proceed slowly."
elif beginning == 2:
    beginning = "bustling castle, wrought forth from stone, able to weather anything."
    onechoice1 = "Chat with the locals."
    onechoice2 = "Start a fight at the tavern."
    onechoice3 = "Try to talk to the king."
    onechoice4 = "Wage war against these hethens!"
elif beginning == 3:
    beginning = "wizard's tower, tall and inquisitive, it lay forboding of dark intellect."
    onechoice1 = "Knock lightly on the door."
    onechoice2 = "Peer in through the window."
    onechoice3 = "Try  an amateur spell."
    onechoice4 = "Call upon the church."
elif beginning == 4:
    beginning = "small peasant's village, filled to the brim with the sick and dying."
    onechoice1 = "Vomit from the smell."
    onechoice2 = "Get mugged by peasants."
    onechoice3 = "Lose yourself in gambling."
    onechoice4 = "Yell at the top of your lungs."


#Here are the print statements which reference the beginning and choice values
print("Welcome to Brayden's Text Story Game.\nIn this game you will be given choices, and with those choices you will influence your outcome.\nPay close attention to the details in the text provided and make sure to follow instructions.");
print("Hello adventurer, standing before you lies a", beginning)
print("What will you do?")
print("1.", onechoice1)
print("2.", onechoice2)
print("3.", onechoice3)
print("4.", onechoice4)
pchoice = int(input("Enter a number: ")) #pchoice is a reusable value


if pchoice == 1 and outcome == 1: #if both pchoice and outcome equal a certain value, another text statement is displayed
    tree = 1
    print("You arm yourself with a club! A formiddable weapon and delve deeper into the darkness. Further down you begin to hear scratching at the cave walls around you.")
    print("What do you do?")
    print("1. Go mad, lose yourself and draw incoherent characters upon the walls with your finger nails and blood.")
    print("2. Fight back the shadows! Triumph over dark!")
    print("3. Meditate.")
    pchoice = int(input("Enter a number: "))
    if pchoice == 1 and tree == 1:
        print("You clambor against the walls, scratching feverishly for some solution, and that's when you find it.\nA glowing aura emanating from the rocks, you spend the rest of your life guarding this new secret.\nTHE END.")
    elif pchoice == 2 and tree == 1:
        print("You swing your club wildly into the darkness, hitting at the shadows that consume all light.\nThe only sound was the swooshing of the club through loose air.\nYou tire yourself out critically and lay down to take your final breaths.\n THE END.")
    elif pchoice == 3 and tree == 1:
        print("You sit down and set your club at your side.\nCalm thoughts, calm mind, calm body...\nYou drift off to thoughts of who you truly are and what you are doing here...\nYour thoughts leave you defenseless, but you are at this point too intellectually strong to fight.\nHordes and hordes of shadow enemies come out from the dark.\nNone can penetrate your mind field, and they all dissolve upon contact.\nThe people nearby this cave will remember your good deeds.\nTHE END! GOOD END!")
elif pchoice == 2 and outcome == 1:
    print("You cower back and run away home, never to return a warrior again.\n THE END! DID YOU EVEN TRY?")
elif pchoice == 3 and outcome == 1:
    print("You rush in swinging your club wildly around, smacking stone after stone, sparks from rocks briefly lighting up the cave.\nAfter your heroic spill you realize you are lost, terribly lost.\nYou are trapped within a maze.")
    while pchoice == 3 and outcome == 1:
        print("1. Left.")
        print("2. Right.")
        mazechoice = int(input("Which way do you go?: "))
        if mazechoice == 1:
            print("Down left you go, to a dead end, but when you turn back around, it is also a dead end. You are trapped with no escape.\nTHE END!")
        elif mazechoice == 2:
            print("Down right you go, to a dead end, but when you turn back around, it is also a dead end. You are trapped with no escape.\nTHE END!")
        break
elif pchoice == 4 and outcome == 1:
    print("You light a torch and realize that the entire cave was actually filled to the brim with spiders.\nThey swarm you before you can react.\nTHE END!")


#This is the endpoint of the first choice loop, cave storyline

if pchoice == 1 and outcome == 2: #for outcome 2, castle storyline
    print("You meet with a peasant and briefly talk about the town he lives in.\nHe tells you to bug off almost immediately.")
    print("What do you do?")
    print("1. Bug off.")
    print("2. Punch him rightly.")
    pchoice = int(input("Enter a number: "))
    if pchoice == 1:
        print("You bug off like the insect you are, never to be taken seriously again. BUZZZZ.")
    elif pchoice == 2:
        print("You sucker punch the peasant directly in the face! That has got to hurt. Guards surround you quickly.")
        print("What do you do?")
        print("1. Punch.")
        pchoice = int(input("Enter a number: "))
        if pchoice == 1:
            print("PUNCH. PUNCH. PUNCH. You... surprisingly? Felled an entire guard group, congratulations!\nYou are now soaked in guards' blood and filled with uncontrollable rage.\nYou continue to punch until there is no more...\nTHE END.")
elif pchoice == 2 and outcome == 2:
    print("You start a fight at the tavern! However, one outsider is not fairly matched against multiple drunk barmates. You are quickly surrounded.\nYou die from blunt force trauma.\nTHE END!")
elif pchoice == 3 and outcome == 2:
    print("You try to speak with the king.\nHe seems far too busy for someone of your reputation, but he obliges you.")
    print("What do you say?")
    print("1. 'HI KING.'")
    print("2. 'I want to rule your kingdom.'")
    pchoice = int(input("Enter a number: "))
    if pchoice == 1:
        print("The king kills you with his magical stare. THE END!")
    elif pchoice == 2:
        print("The king looks at you very strangely, and then turns away.\nThough when you look at the ground where he left, he left you a tiny version of a kingdom.\nIt is yours now to rule.\nTHE END!")
elif pchoice == 4 and outcome == 2:
    print("Fire, brimstone, steel against steel. You've caused one of the greatest calamities in history with this attack.\nNot a single person was spared.\nNot even you.\nTHE END!")

#This is the endpoint of the second choice loop, castle storyline

if pchoice == 1 and outcome == 3: #for outcome 3, wizard storyline
    print("The door creaks open by itself inside.\nYou explore the room which is filled to the brim with experiments, test tubes, and alchemy.")
    print("What do you do?")
    print("1. Steal the spellbook!")
    print("2. Conjure an ancient spirit with ingredients from the tower.")
    pchoice = int(input("Enter a number: "))
    if pchoice == 1:
        print("You attempt to steal the spellbook, however upon closer notice, it isn't a spellbook.\nIt is the NECRONOMICON!\nYou are consumed by your own insanity from witnessing the book.\nTHE END!")
    elif pchoice == 2:
        print("You conjure an ancient spirit! This spirit however is already bound to someone else.\nThey will cut you a deal though, and grant you one wish.")
        print("What do you do?")
        print("1. 'I wish for world peace!'")
        print("2. 'I wish for world dominance!'")
        pchoice = int(input("Enter a number: "))
        if pchoice == 1:
            print("The world shatters at the core, and you are given a piece.\nTHE END!")
        elif pchoice == 2:
            print("The world is now the dominant world in all of existence.\nMeaning it is a huge planet.\nTHE END!")
elif pchoice == 2 and outcome == 3:
    print("You look in through a window and see you have no reflection.\nHow could this be you ask?\nOn further examination you realize you are inside of the mirror now!\nWith no way out of this mirror world you exist only now as your reflection...\nTHE END!")
elif pchoice == 3 and outcome == 3:
    print("You attempt an amateur spell off the top of your head.\nThe door in front of you combusts into flames!\nNear you appears the wizard, and he is not happy.\nHe turns you into a frog.\nTHE END!")
elif pchoice == 4 and outcome == 3:
    print("You call upon the church.\nThey immediately notice the evil aura this tower gives off.\nThey rush in with you at their side to confront their enemy.\nThe wizard shows, levitating off the ground and crackling at his hands with electricity.")
    print("What do you do?")
    print("1. Ground yourself!")
    print("2. Use a mirror to reflect!")
    pchoice = int(input("Enter a number: "))
    if pchoice == 1:
        print("You ground yourself and avoid being shocked alive.\nHowever your church friends aren't so lucky.\nOne on one you are overwhelmed by the power of the wizard...\nTHE END!")
    elif pchoice == 2:
        print("You grab a mirror and reflect the electricity back into the wizard!\nExcept the electricity isn't being reflected, it is being absorbed...\nThe wizard is sucked into the mirror and locked away forever!\nTHE END!")

#This is the endpoint of the third choice loop, wizard storyline


if pchoice == 1 and outcome == 4:
    print("You vomit out your guts onto the floor and collapse.\nTHE END!")
elif pchoice == 2 and outcome == 4:
    print("You are mugged by peasants who steal everything but your underwear.\nWith no money you are forced to live this same life.\nTHE END!")
elif pchoice == 3 and outcome == 4:
    print("You gamble, it is a simple guessing game. Red or black.")
    print("1. Red.")
    print("2. Black.")
    coin = random.randint(1,2)
    pchoice = int(input("Enter a number: "))
    if pchoice == 1:
        if coin == 1:
            print("You win! Congratulations!\nYou live the rest of your life in luxury.\nTHE END")
        elif coin == 2:
            print("You lose! You spend the rest of your life in poverty.\nTHE END")
    if pchoice == 2:
        if coin == 1:
            print("You lose! You spend the rest of your life in poverty.\nTHE END")
        elif coin == 2:
            print("You win! Congratulations!\nYou live the rest of your life in luxury.\nTHE END")
elif pchoice == 4 and outcome == 4:
    print("You couldn't handle this... You yelled at the top of your lungs.\nYou peak your vocal cords and tear them from the stress.\nYou are mute to the world, forever.\nTHE END!")
