def is_match(first_argument, second_argument):
    firstID = 0  # index in first_argument
    secondID = 0  # index in second_argument

    second_star = -1  # To stall/keep secondID value when first_argument is longer than second_argument
    star = 0   # Used to push 1stID
    # Go through all of the first Argument.
    # Continue until firstID is smaller than length of first argument(String).
    while firstID < len(first_argument):
        print("firstID: ", firstID, " ,secondID: ", secondID, " ,second_star: ", second_star, " ,star: ", star)

        # Add 1 to 1stID and 2ndID IF 2ndID is less than length of 2nd argument AND
        if secondID < len(second_argument) and (
                first_argument[firstID] == second_argument[secondID] or second_argument[secondID] == '?'):
            firstID += 1
            secondID += 1
        # Else If 2ndID is less than length of second arg AND second argument's letter at secondID (index) equals '*'.
        # Simply: Ignore '*' sign in second argument.
        elif secondID < len(second_argument) and second_argument[secondID] == '*':
            second_star = secondID
            secondID += 1
            star = firstID
        # Else if: star value IS NOT -1 (& none of above IFs did not fire), set 2ndID to star+1, 2nd_star up by one
        # AND set 1stID to 2nd_star value.
        # Simply: by using star & 2nd_star loop can go back on 2nd argument while pushing 1stID.
        elif second_star != -1:
            # print("branch fired")
            secondID = second_star + 1
            star += 1
            firstID = star
        # If none of the ABOVE IF's fire return False.
        else:
            return False
    # Second loop - while 2ndID is less than length of 2nd argument AND at index(2ndID) in 2nd argument the sign is
    # '*' - up 2ndID by 1.
    while secondID < len(second_argument) and second_argument[secondID] == '*':
        secondID += 1
    # Return true if 2ndID equals length of second argument.
    # Main return statement
    return secondID == len(second_argument)


# Return True
print(is_match('abab', 'ab*ab'))
print(is_match('abzyzab', 'ab*ab'))
print(is_match('abzzzab', 'ab???ab'))
print(is_match('aba1a2a3a4a5a6ab', 'ab*ab'))

# Return False
print(is_match('abab1', 'abab'))
print(is_match('abzzzab', 'ab???aby'))
print(is_match('abab', 'a***********asbsbsdf'))
