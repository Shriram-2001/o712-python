from rand_question_v3.data import name_list, questions
from rand_question_v3.selector import random_choice

def main():
    remaining_names = name_list.copy()

    while True:
        to_cont = input("Enter 'Y' to continue, any other key to stop: ") 

        if to_cont.upper() != 'Y':
            break
        
        result = random_choice(remaining_names, questions)

        print(result)
        chosen_name = result.split("**")[1]
        remaining_names.remove(chosen_name)

        if len(remaining_names) == 0:
            print("All names have been chosen.")
            break

    