import random
import heapq
from colorama import Fore, Style, init

def load_word_list(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_feedback(guess, secret):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            feedback.append("G")  # Correct letter in the correct place
        elif guess[i] in secret:
            feedback.append("Y")  # Correct letter in the wrong place
        else:
            feedback.append("B")  # Incorrect letter
    return feedback

def heuristic(word, possible_words):
    # Simple heuristic: count how many unique letters are in the word
    return len(set(word))

class Node:
    def __init__(self, word, possible_words, parent=None):
        self.word = word
        self.possible_words = possible_words
        self.parent = parent
        self.cost = 0
        self.heuristic = heuristic(word, possible_words)
        self.f = self.cost + self.heuristic

    def __lt__(self, other):
        return self.f < other.f

def a_star_search(possible_words, secret_word):
    open_set = []
    closed_set = set()

    # Start with an initial guess (arbitrarily chosen)
    initial_guess = random.choice(possible_words)
    start_node = Node(initial_guess, possible_words)
    
    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.word == secret_word:
            return current_node.word  # Found the solution

        closed_set.add(current_node.word)

        # Generate new guesses based on feedback
        feedback = get_feedback(current_node.word, secret_word)

        for word in current_node.possible_words:
            if word in closed_set:
                continue

            # Filter possible words based on feedback
            new_possible_words = filter_words(current_node.possible_words, current_node.word, feedback)
            if new_possible_words:
                new_node = Node(word, new_possible_words, current_node)
                heapq.heappush(open_set, new_node)

    return None  # No solution found

def filter_words(possible_words, guess, feedback):
    filtered_words = []
    for word in possible_words:
        match = True
        for i in range(len(guess)):
            if feedback[i] == "G" and guess[i] != word[i]:
                match = False
                break
            elif feedback[i] == "Y" and (guess[i] not in word or guess[i] == word[i]):
                match = False
                break
            elif feedback[i] == "B" and guess[i] in word:
                match = False
                break
        if match:
            filtered_words.append(word)
    return filtered_words

# Initialize colorama
init(autoreset=True)

def play_wordle():
    # Select difficulty level
    print("Choose difficulty level:")
    print("1. Easy (4-letter words)")
    print("2. Normal (5-letter words)")
    print("3. Hard (7-letter words)")
    choice = input("Enter your choice (1, 2, or 3): ").strip()

    if choice == '1':
        word_length = 4
        word_list_file = 'WORD_LIST1.txt'
    elif choice == '2':
        word_length = 5
        word_list_file = 'WORD_LIST2.txt'
    elif choice == '3':
        word_length = 7
        word_list_file = 'WORD_LIST3.txt'
    else:
        print("Invalid choice. Defaulting to Normal (5-letter words).")
        word_length = 5
        word_list_file = 'WORD_LIST2.txt'

    # Load the appropriate word list
    WORD_LIST = load_word_list(word_list_file)

    if not WORD_LIST:
        print(f"No words of length {word_length} found in the word list.")
        return

    # Select a random word from the filtered list
    correct_word = random.choice(WORD_LIST)
    attempts = 6  # Number of attempts allowed
    previous_feedback = []

    print("Welcome to Wordle!")
    print(f"You have {attempts} attempts to guess the correct word.")

    for attempt in range(attempts):
        guess = input(f"Attempt {attempt + 1}: Enter your guess: ").strip().lower()
        
        if len(guess) != len(correct_word):
            print(f"Your guess must be {len(correct_word)} letters long.")
            continue
        
        feedback = get_feedback(guess, correct_word)
        colored_feedback = []

        for i, char in enumerate(guess):
            if feedback[i] == "G":
                colored_feedback.append(Fore.GREEN + char + Style.RESET_ALL)
            elif feedback[i] == "Y":
                colored_feedback.append(Fore.YELLOW + char + Style.RESET_ALL)
            else:
                colored_feedback.append(Fore.RED + char + Style.RESET_ALL)

        feedback_str = "Feedback: " + "".join(colored_feedback)
        
        previous_feedback.append(feedback_str)
        for feedback in previous_feedback:
                print(feedback)

        if guess == correct_word:
            print(f"Congratulations! You've guessed the word '{correct_word}'.")
            return
        
    print(f"Sorry, you've run out of attempts. The correct word was '{correct_word}'.")

if __name__ == "__main__":
    play_wordle()