import random
import heapq
from colorama import Fore, Style, init

# Sample word list
WORD_LIST = ["apple", "grape", "peach", "berry", "melon", "mango", "lemon", "cherry", "plum", "kiwi"]

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

def a_star_search(possible_words, target_word):
    open_set = []
    closed_set = set()

    # Start with an initial guess (arbitrarily chosen)
    initial_guess = random.choice(possible_words)
    start_node = Node(initial_guess, possible_words)
    
    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.word == target_word:
            return True  # Found the word

        closed_set.add(current_node.word)

        for word in current_node.possible_words:
            if word in closed_set:
                continue

            new_node = Node(word, possible_words, current_node)
            heapq.heappush(open_set, new_node)

    return False  # Word not found

# Initialize colorama
init(autoreset=True)

def play_wordle():
    # Select a random word from the WORD_LIST
    correct_word = random.choice(WORD_LIST)
    attempts = 6  # Number of attempts allowed
    previous_feedback = []

    print("Welcome to Wordle!")
    print(f"You have {attempts} attempts to guess the correct word.")

    for attempt in range(attempts):
        guess = input(f"Attempt {attempt + 1}: Enter your guess: ").strip().lower()

        # Check if the guessed word exists in the word list using A* search
        if not a_star_search(WORD_LIST, guess):
            print("The guessed word is not in the word list. Please try again.")
            continue

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