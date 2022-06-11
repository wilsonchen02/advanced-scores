# User gets randomly generated result
import random

# Coin flip (head/tails)
def flip_coin():
    if random.randint(0, 1) == 0:
        print('Heads\n')
    else:
        print('Tails\n')

# Dice roll (1-6)
def dice_roll():
    print('You rolled a ' + str(random.randint(1, 6)) + '\n')

# 8 ball
messages = ['It is certain',
    'It is decidedly so',
    'Yes definitely',
    'Reply hazy try again',
    'Ask again later',
    'Concentrate and ask again',
    'My reply is no',
    'Outlook not so good',
    'Very doubtful']


# Driver
def main():
    print('The user gets to choose what random result they want to generate.')
    while True:
        print('Select an option:')
        print('\tcoin')
        print('\tdice')
        print('\t8ball')
        user_input = input('Your input: ')

        if user_input == 'coin':
            flip_coin()
        elif user_input == 'dice':
            dice_roll()
        elif user_input == '8ball':
            print(random.choice(messages) + '\n')
        else:
            print('Invalid option\n')
        
        # Ask user if they want to continue
        print('Keep going? (y/n)')
        user_input = input('Your input: ')
        if user_input == 'y':
            continue
        elif user_input == 'n':
            exit()
        else:
            print('Invalid option\n')

if __name__ == "__main__":
    main()