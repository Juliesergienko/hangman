# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"
all_letters = string.ascii_lowercase
vowels = "aeiou"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter in letters_guessed:
            continue
        else:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = ""
    for letter in secret_word:
        if letter in letters_guessed:
            result += letter + ' '
        else:
            result += "_ "
    return result.strip()




def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    return ''.join([letter for letter in all_letters if letter not in letters_guessed])



def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_left = 6
    warnings_left = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long".format(len(secret_word)))
    print(get_guessed_word(secret_word, letters_guessed))
    while guesses_left:
        print("You have {} guesses left".format(guesses_left))
        print("Available letters: {}".format(get_available_letters(letters_guessed)))
        user_input_valid = False
        while not user_input_valid:
            user_input = input("Please guess a letter: ")
            error_message = ""
            if len(user_input) > 1:
                error_message = "Sorry, you can type only 1 letter."
            if not user_input.isalpha():
                error_message = "Oops! That is not a valid letter."
            if user_input.lower() in letters_guessed:
                error_message = "Oops! You've already guessed that letter."

            if error_message:
                warnings_left -= 1
                if warnings_left < 0:
                    guesses_left -= 1
                    print("{} You have no warnings left so you lose one guess. You have {} guesses left.".format(error_message, guesses_left))
                else:
                    print("{} You have {} warnings left: {}".format(
                        error_message, warnings_left, get_guessed_word(secret_word, letters_guessed)
                    ))
            else:
                user_input_valid = True

        user_input = user_input.lower()
        letters_guessed.append(user_input)
        if user_input in secret_word:
            print("Good guess: {}".format(get_guessed_word(secret_word, letters_guessed)))
        elif user_input in vowels:
            guesses_left -= 2
            print("Oops! That letter is not in my word: {}".format(get_guessed_word(secret_word, letters_guessed)))
        else:
            guesses_left -= 1
            print("Oops! That letter is not in my word: {}".format(get_guessed_word(secret_word, letters_guessed)))

        print("------------")
        if is_word_guessed(secret_word, letters_guessed):
            total_score = guesses_left * len(set(secret_word))
            print("Congratulations, you won!")
            print("Your total score for this game is: {}".format(total_score))
            return
    print("Sorry, you ran out of guesses. The word was {}.".format(secret_word))
    return



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = ''.join([i for i in my_word if i != ' '])
    if len(my_word) != len(other_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] == '_':
            if other_word[i] in my_word:
                return False
            else:
                continue
        if my_word[i] != other_word[i]:
            return False
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    result = ""
    for word in wordlist:
        if match_with_gaps(my_word, word):
            result += word + ' '
    if result:
        print(result.strip())
    else:
        print("No matches found")




def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_left = 6
    warnings_left = 3
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {} letters long".format(len(secret_word)))
    print(get_guessed_word(secret_word, letters_guessed))
    while guesses_left:
        print("You have {} guesses left".format(guesses_left))
        print("Available letters: {}".format(get_available_letters(letters_guessed)))
        user_input_valid = False
        while not user_input_valid:
            user_input = input("Please guess a letter: ")
            error_message = ""
            if user_input == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                continue
            if len(user_input) > 1:
                error_message = "Sorry, you can type only 1 letter."
            if not user_input.isalpha():
                error_message = "Oops! That is not a valid letter."
            if user_input.lower() in letters_guessed:
                error_message = "Oops! You've already guessed that letter."

            if error_message:
                warnings_left -= 1
                if warnings_left < 0:
                    guesses_left -= 1
                    print("{} You have no warnings left so you lose one guess. You have {} guesses left.".format(error_message, guesses_left))
                else:
                    print("{} You have {} warnings left: {}".format(
                        error_message, warnings_left, get_guessed_word(secret_word, letters_guessed)
                    ))
            else:
                user_input_valid = True

        user_input = user_input.lower()
        letters_guessed.append(user_input)
        if user_input in secret_word:
            print("Good guess: {}".format(get_guessed_word(secret_word, letters_guessed)))
        elif user_input in vowels:
            guesses_left -= 2
            print("Oops! That letter is not in my word: {}".format(get_guessed_word(secret_word, letters_guessed)))
        else:
            guesses_left -= 1
            print("Oops! That letter is not in my word: {}".format(get_guessed_word(secret_word, letters_guessed)))

        print("------------")
        if is_word_guessed(secret_word, letters_guessed):
            total_score = guesses_left * len(set(secret_word))
            print("Congratulations, you won!")
            print("Your total score for this game is: {}".format(total_score))
            return
    print("Sorry, you ran out of guesses. The word was {}.".format(secret_word))
    return


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
