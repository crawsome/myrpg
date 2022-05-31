# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Hero:
    def __init__(self, name, b_mo, hp=10, mp=5, gold=0):
        self.name = name
        self.birthday_month = b_mo
        self.hp = hp
        self.mp = mp
        self.gold = 0
        self.greet()

    def heal(self):
        pass

    def hurt(self):
        pass

    def greet(self):
        print(f'Hello {self.name}, \nwelcome to the world of your own imagination!')
        print(f'I\'m happy you can be here, how lovely someone born in {self.birthday_month} could be so polite!')




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def camp():
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Credits Screen
    print('Welcome to MyRPG!\nColin Burke 2022!\nApril RPG Game Jam!\nLike and Subscribe!')

    # Get user's name
    user_name = input('Please enter your name, brave traveler!')

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']

    month = ''
    # Get user's birthday month
    while month not in months:
        month = str(input('Please type your birth month')).lower()
        if month not in months:
            print('Not a valid month, try again')

    # Instantiate Hero object

    our_hero = Hero(user_name,month)



# Game loop
