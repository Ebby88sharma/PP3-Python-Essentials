import curses
import random
import os

""" Snake Game Instructions"""
def snake_instructions():
    print("\n--- Snake Game Instructions ---")
    print("1. Use the arrow keys to move the snake.")
    print("2. Your goal is to eat the food (represented by π) to grow your snake.")
    print("3. Avoid crashing into the walls or your own tail.")
    print("4. The game ends when you hit the wall or yourself.")
    print("5. Press Enter to start the game.\n") 
    input("Press Enter to start the game...")

"""Rock-Paper-Scissors Instructions """
def rps_instructions():
    print("\n--- Rock-Paper-Scissors Instructions ---")
    print("1. You will be asked to choose between Rock, Paper, or Scissors.")
    print("2. Type 'R' for Rock, 'P' for Paper, or 'S' for Scissors.")
    print("3. The computer will randomly select one of the options.")
    print("4. Rock beats Scissors, Scissors beats Paper, and Paper beats Rock.")
    print("5. Press Enter to start the game.\n")  
    input("Press Enter to start the game...")

"""General Instructions (for both games)"""
def general_instructions():
    print("\n--- Game Instructions ---")
    print("Choose a game to play:")
    print("1. Snake Game")
    print("   - Use the arrow keys to move.")
    print("   - Avoid walls and your own tail.")
    print("   - Eat food to grow.")
    print("2. Rock-Paper-Scissors")
    print("   - Rock beats Scissors.")
    print("   - Paper beats Rock.")
    print("   - Scissors beats Paper.")
    print("After each game, you'll be asked if you want to play again.")
    input("Press Enter to go back to the menu...")

""" Snake Game """
def play_snake(screen):
    """ Setup screen """
    try:
        curses.curs_set(0) 
    except curses.error:
        pass 

    screen_height, screen_width = screen.getmaxyx()  
    window = curses.newwin(screen_height, screen_width, 0, 0) 
    window.keypad(1) 
    window.timeout(100)

    """ Initial position for snake's head"""
    snake_x = screen_width // 4
    snake_y = screen_height // 2

    """ Initial snake body """
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    """ initial food position """
    food = [screen_height // 2, screen_width // 2]
    window.addch(food[0], food[1], curses.ACS_PI)  

    """ Set the initial direction of snake movement """
    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = window.getch() 
        key = key if next_key == -1 else next_key 

        """ Check if snake has hit the border or itself """
        if (
            snake[0][0] in [0, screen_height - 1] or  
            snake[0][1] in [0, screen_width - 1] or 
            snake[0] in snake[1:] 
        ):
            curses.endwin()
            print(f"Game Over! Final Score: {score}")
            break

        """ Calculation for the new position of the snake's head """
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        """ Insert the new head to the snake """
        snake.insert(0, new_head)

        """ Check if snake has eaten the food """
        if snake[0] == food:
            score += 1 
            food = None
            while food is None:
                new_food = [
                    random.randint(1, screen_height - 2),
                    random.randint(1, screen_width - 2)
                ]
                food = new_food if new_food not in snake else None
            window.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        """ Ensure the snake's head is within bounds before drawing it """
        if 0 < snake[0][0] < screen_height - 1 and 0 < snake[0][1] < screen_width - 1:
            window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD) 

        """ Display the score at the top left """
        window.addstr(0, 0, f'Score: {score}')


""" Rock-Paper-Scissors Game """
def determine_winner(player, computer):
    if player == computer:
        return "It's a draw!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "You win!"
    else:
        return "Computer wins!"

""" Function to validate player input """
def get_player_choice():
    choices = {"r": "rock", "p": "paper", "s": "scissors"}
    while True:
        player_choice = input("Choose (R)ock, (P)aper, or (S)cissors: ").lower()
        if player_choice in choices:
            return choices[player_choice]
        else:
            print("Invalid input. Please choose 'R', 'P', or 'S'.")

""" Main game loop for Rock-Paper-Scissors """
def play_rock_paper_scissors():
    print("Welcome to Rock, Paper, Scissors!")
    while True:
        player_choice = get_player_choice()
        computer_choice = random.choice(["rock", "paper", "scissors"])

        print(f"\nYou chose: {player_choice}")
        print(f"Computer chose: {computer_choice}")

        result = determine_winner(player_choice, computer_choice)
        print(f"Result: {result}\n")

        play_again = input("Do you want to play again? (Y/N): ").lower()
        if play_again != "y":
            print("Thanks for playing!")
            break


""" Main Menu to choose between the games and instructions """
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Snake Game")
        print("2. Rock-Paper-Scissors")
        print("3. Instructions")
        choice = input("Enter the number of your choice (1, 2, or 3): ")

        if choice == '1':
            snake_instructions()
            curses.wrapper(play_snake)  
        elif choice == '2':
            rps_instructions()
            play_rock_paper_scissors()
        elif choice == '3':
            general_instructions()
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

        """ Ask the user if they want to play again or switch games """
        play_again = input("Do you want to play another game? (Y/N): ").lower()
        if play_again != 'y':
            print("Thanks for playing! Goodbye!")
            break


""" Start the program with the main menu """
if __name__ == "__main__":
    main_menu()
