'''
import random
import os
import ast

words_main_list = [
    ("apple", "easy"), ("banana", "easy"), ("orange", "easy"), ("grape", "easy"), ("kiwi", "easy"),
    ("strawberry", "easy"), ("blueberry", "easy"), ("pineapple", "easy"), ("watermelon", "easy"),
    ("elephant", "medium"), ("guitar", "medium"), ("banana", "medium"), ("rabbit", "medium"), ("lemon", "medium"),
    ("turtle", "medium"), ("rainbow", "medium"), ("dragon", "medium"), ("pizza", "medium"), ("camera", "medium"),
    ("dragonfly", "medium"), ("butterfly", "medium"), ("diamond", "medium"), ("pirate", "medium"), ("laptop", "medium"),
    ("coffee", "medium"), ("tiger", "medium"), ("snowman", "medium"), ("dolphin", "medium"),
    ("velociraptor", "hard"), ("rhinoceros", "hard"), ("zucchini", "hard"), ("quadrilateral", "hard"),
    ("mysterious", "hard"), ("cacophony", "hard"), ("pharaoh", "hard"), ("eccentric", "hard"), ("algorithm", "hard"),
    ("serendipity", "hard"), ("exquisite", "hard"), ("hieroglyphic", "hard"), ("bureaucracy", "hard"),
    ("resplendent", "hard"), ("pterodactyl", "hard"), ("labyrinth", "hard"), ("synonymous", "hard"),
    ("belligerent", "hard"), ("camouflage", "hard"), ("hemorrhage", "hard")
]

hangman_stages = [
    """
       +---+
           |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]                                                                               #attempt to draw a hanged stickman

def create_and_append_dicts(file, d1):
    try:
        file_exists = os.path.exists(file)  #O(1)
        if file_exists == True:
            print("Game started")           #check if the file already exists
            return
        
        
        with open(file, "a") as file:
            if not file_exists:                        #O(n) = n is the size of the text
                file.write("## Dictionary ##\n")      #open the file in append mode (or create it if it doesn't exist)
            
            
            file.write("dict1 = " + str(d1) + "\n")    #O(n), write the words into the file
        
        print("Properties file created!")
    except Exception as e:
        print("An error occurred:", e)

create_and_append_dicts("Properties.txt", words_main_list)

def get_dictionary_from_file(file_name, dict_number):
    try:  
        with open(file_name, "r") as file:
            file_contents = file.read()         #open the file and read its contents
        
        start_index = file_contents.find(f"dict{dict_number} = ")
        if start_index == -1:
            raise ValueError(f"Dictionary 'dict{dict_number}' not found in the file.")  #find the start and end positions of the dictionary with the specified number

        end_index = file_contents.find("\n", start_index)
        if end_index == -1:
            end_index = len(file_contents)

        dict_expression = file_contents[start_index + len(f"dict{dict_number} = "):end_index]   #extract the dictionary expression
        dictionary = ast.literal_eval(dict_expression) #convert the dictionary expression to a dictionary object

        return dictionary                             #O(n): all of this depends on the size of the dictionary and the size of the file to read

    except FileNotFoundError:
        print("File not found.")
    except ValueError as e:
        print("Error:", e)
    except SyntaxError as e:
        print("Error parsing dictionary:", e)

file1_name = "Properties.txt"
dicty1 = 1

def append_to_dict(file_name, key, value):
    try:
        with open(file_name, "r") as file:          #read the contents of the file
            file_contents = file.read()
        
        start_index = file_contents.find("dict1 = ")        #find the position of the dictionary in the file
        if start_index == -1:
            raise ValueError("Dictionary 'dict1' not found in the file.")

        dict_expression = file_contents[start_index + len("dict1 = "):] # Extract the dictionary expression
        dict_list = eval(dict_expression)           #convert the dictionary expression to a list of tuples
        my_dict = dict(dict_list)                   #convert the list of tuples to a dictionary
        my_dict[key] = value                        #append the new key-value pair

        with open(file_name, "w") as file:          #write the updated dictionary back to the file
            file.write("dict1 = " + str(list(my_dict.items())) + "\n")

    except FileNotFoundError:
        print("File not found.")
    except ValueError as e:
        print("Error:", e)                  
                                                    #same case O(n) because it depends on the size of the dictionary

def add_word():
    while True:
        word = input("Enter the new word: ").lower()
        
        if any(word == existing_word for existing_word, _ in word_dictionary): #"if any()"" will return True if any of the iterables existingword is already in words
            print("Word '{}' is already on the list".format(word))
            response = input("Do you want to add another word? (yes/no): ").lower()
            if response == "yes":
                return add_word()
            else:
                return play()
            
        if not word.isalpha():
            print("Please, only words")
        else:
            while True:
                difficulty = input("Enter the difficulty level (easy/medium/hard): ").lower()
                if difficulty in ["easy", "medium", "hard"]:
                    append_to_dict(file1_name, word, difficulty)
                    print("Word '{}' with difficulty '{}' added successfully!".format(word, difficulty))
                    response = input("Do you want to add another word? (yes/no): ").lower()
                    if response == 'yes':
                        return add_word()
                    else:
                        return play()
                else:
                    print("Dude, you can only enter 'easy', 'medium', or 'hard' as difficulty.")            #O(n)= where n is the lenght of the function

word_dictionary = get_dictionary_from_file(file1_name, dicty1)

def choose_word(difficulty):
    filtered_words = [word for word, level in word_dictionary if level == difficulty]    #Choose a random word from the list with the specified difficulty using list comprehension to filter by difficulty
    return random.choice(filtered_words)  #the list comprenhension has a O(n), but the ramdomizer is O(1)

def display_word(word, guessed_letters):
    display = ""
    for letter in word:             #iterating within the letters of the ramdom word chosen
        if letter in guessed_letters:       #this has O(n) becuase it depends on the lenght of the word
            display += letter
        else:
            display += "_"          #if the word has been guessed, it will display it, if not it will display _
    return display                  #Display the word with underscores for unguessed letters

def play():
    while True:
        difficulty = input("To play, first choose difficulty (easy/medium/hard): ").lower()
        if difficulty in ["easy", "medium", "hard"]:    #validate the answer is between the options
            break
        else:
            print("Invalid input! Please enter 'easy', 'medium', or 'hard'.")
    word = choose_word(difficulty) #this has a time complex of O(n)
    print("Alright, lets play")
    print("The word has {} letters.".format(len(word)))
    guessed_letters = []            #list of all the letters "input" by the user
    failures = 7 # Number of failures allowed
    errors= 0 
    total_attempts= 0
    hangman_stage = 1  # Initial hangman stage
    
    print(hangman_stages[hangman_stage])  # Display initial hangman stage, #this first part has a O(1) complex

    while True:
        print("\nWord:", display_word(word, guessed_letters)) #uses the display function to show the words (with letters and underscores)
        guess = input("Guess a letter: ").lower()
        guess_lenght = len(guess)

        if guess in guessed_letters:
            print(hangman_stages[hangman_stage])
            print("You already guessed that letter.")   #validate if the letter has been already entered by checking in the list guessed_letters[]
            total_attempts += 1
        elif not guess.isalpha():                       #validate the input is a letter
            print(hangman_stages[hangman_stage])        #print current hangman stage
            print("You can only enter letters!")
            total_attempts += 1
            continue                                    #skip this and continue for a new guess
        elif guess_lenght >1:                           #validate the input is only one letter
            print(hangman_stages[hangman_stage])
            print("You can only enter one letter at the time!")
            total_attempts += 1
        elif guess in word:                             #correct input, append the guess to the list
            print(hangman_stages[hangman_stage])        #print current hangman stage
            print("Correct!")
            total_attempts += 1
            guessed_letters.append(guess)
        else:
            print("Incorrect!")
            hangman_stage += 1                          #update the status of hangman
            print(hangman_stages[hangman_stage])        #print current hangman stage
            failures -= 1
            errors += 1                                 #reduce the number of failures available
            total_attempts += 1
            guessed_letters.append(guess)               #incorrect input, append the guess to the list

        if "_" not in display_word(word, guessed_letters):              #check if there are no more letters to guess, so the player wins
            print(hangman_stages[hangman_stage])
            correct_ratio= round(100-((errors/total_attempts)*100))
            print("Congratulations! You guessed the word: {} in a total of {} attempts and {} errors! (That is a {}% of correct guesses :O)".format(word, total_attempts, errors,correct_ratio))
            break
        elif failures == 0:                                               #check if the player has lost
            correct_ratio= round(100-((errors/total_attempts)*100))
            print("Dude you let hangman die :( The word was: {}... very close. You made a total of {} attempts and {} errors. This is a {}% of correct guesses".format(word,total_attempts, errors,correct_ratio))
            break

        print("Wrong Attempts left:", failures)         #O(length of the word+number of letters guessed+size of the filtered list by difficulty)

    play_again = input("Do you want to start again? (yes/no): ").lower() #check if the player wants too play again
    if play_again == "yes":                             
        start()
    else:
        print("Ok, bye")

def start():
    first_question = input("Do you want to add a word before playing?: ")
    if first_question == 'yes':
        return add_word()
    else:
        return play()                       #O(1)

start()
'''

#Run this prior to starting the exercise
from random import randint as rnd

memReg = '/members.txt'
exReg = '/inactive.txt'
fee =('yes','no')

def genFiles(current,old):
    with open(current,'w+') as writefile: 
        writefile.write('Membership No  Date Joined  Active  \n')
        data = "{:^13}  {:<11}  {:<6}\n"

        for rowno in range(20):
            date = str(rnd(2015,2020))+ '-' + str(rnd(1,12))+'-'+str(rnd(1,25))
            writefile.write(data.format(rnd(10000,99999),date,fee[rnd(0,1)]))


    with open(old,'w+') as writefile: 
        writefile.write('Membership No  Date Joined  Active  \n')
        data = "{:^13}  {:<11}  {:<6}\n"
        for rowno in range(3):
            date = str(rnd(2015,2020))+ '-' + str(rnd(1,12))+'-'+str(rnd(1,25))
            writefile.write(data.format(rnd(10000,99999),date,fee[1]))


genFiles(memReg,exReg)
