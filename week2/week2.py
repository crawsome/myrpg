# This is a sample Python script.
 
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
 
class Hero:
    def __init__(self, name, b_mo, attack=4, hp=40, mp=5, gold=0):
        self.name = name
        self.birthday_month = b_mo
        self.hp = hp
        self.mp = mp
        self.attack = 4
        self.gold = 0
        self.exp = 0
        self.alive = True
        self.greet()
 
    def is_alive(self):
        if self.hp <= 0:
            return False
        else:
            return True
 
    def heal(self):
        pass
 
    def hurt(self):
        pass
 
    def greet(self):
        print(f'Hello {self.name}, \nwelcome to the world of your own imagination!')
        print(f'I\'m happy you can be here, how lovely someone born in {self.birthday_month} could be so polite!')
 
 
class Enemy:
    def __init__(self, name, attack=2, hp=10, gold=0):
        self.name = name
        self.exp = 2
        self.attack = attack
        self.hp = hp
        self.gold = 5
 
    def is_alive(self):
        if self.hp <= 0:
            return False
        else:
            return True
 
 
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
 
    our_hero = Hero(user_name, month)
    our_enemy = Enemy('Feisty Goblin', hp=60)
 
    while our_hero.is_alive():
        print(f'You attack {our_enemy.name} for {our_hero.attack} Damage!')
        our_enemy.hp -= our_hero.attack
        if not our_enemy.is_alive():
 
            print(f'{our_enemy.name} was Defeated!')
 
            print(f'You gained {our_enemy.exp} XP!')
            our_hero.exp += our_enemy.exp
 
            print(f'You gained {our_enemy.gold} Gold!')
            our_hero.gold += our_enemy.gold
 
        print(f'{our_enemy.name} attacks you for {our_enemy.attack} Damage!')
        our_hero.hp -= our_enemy.attack
        if not our_hero.is_alive():
            print(f'You were Defeated!')
 
# Game loop
 
