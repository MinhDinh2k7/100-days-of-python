from pathlib import Path
import pandas

student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

#Looping through dictionaries:
for (key, value) in student_dict.items():
    #Access key and value
    pass

script_dir = Path(__file__).parent
full_path = script_dir / "nato_phonetic_alphabet.csv"

student_data_frame = pandas.read_csv(full_path)

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

#TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}
#Loop through rows of a data frame
NATO_phonetic_alphabet = {row.letter: row.code for (index, row) in student_data_frame.iterrows()}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

def generate_phonetic():
    user_input = input("Enter a word: ").upper()
    try:
        output_list = [NATO_phonetic_alphabet[letter] for letter in user_input]
    except KeyError:
        print("Please enter only letters of the alphabet.")
        user_input = input("Enter a word: ").upper()
        generate_phonetic()
    else:
        print(output_list)

generate_phonetic()