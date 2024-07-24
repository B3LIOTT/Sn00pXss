import random


def random_case(word: str) -> str:
    """
    Return a word with random case
    """
    buffer = ""
    nb_upper = 0
    for char in word:
        # ensure that we have at least one upper case and not all the word is in upper case
        if nb_upper == len(word)-1:
            break
        if char == word[-1] and nb_upper == 0:
            buffer += char.upper()
            break
        
        # pick a random case for alphabetic characters
        if char.isalpha():
            if random.randint(0, 1) == 1:
                buffer += char.upper()
                nb_upper += 1
            else:
                buffer += char.lower()
        else:
            buffer += char

    return buffer
