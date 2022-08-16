import random
from dbsetup import DBSetup
import os


def confirm():
    return 'Press [Enter] to Continue'


def choice(title='Choice:', ls=['Y', 'N']) -> int:
    """
    :param title: string for display
    :param ls: list for user's informed choice
    :return: int of user's index choice of that list
    """
    print(title)
    for index, item in enumerate(ls):
        print(f'{index + 1}: {item}')
    try:
        c = int(input(('Your choice:')))
    # if not within valid results, return first result
    except (ValueError, TypeError):
        print('You typed the selection wrong, marking it one.')
        c = 1
    return c


class Equippable:
    def __init__(self, name: str, slot: int, attack=0, defense=0, hp_mod=0, mp_mod=0, value=0, dur=100):
        self.name = name
        self.slot = slot
        self.base_attack = attack
        self.attack = attack
        self.base_defense = defense
        self.defense = attack
        self.hp_mod = hp_mod
        self.mp_mod = mp_mod
        self.value = value
        self.dur = dur
        self.base_dur = dur


class Actor:
    def __init__(self, name: str, b_mo: str, hp=40, mp=5, attack=4, defense=4):
        self.name = name
        self.b_mo = b_mo
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.alive = True

    def __str__(self) -> str:
        return f'{self.name}, {self.b_mo}, {self.hp}, {self.mp}, {self.attack}, {self.defense}, {self.alive}'

    def hurt(self, incoming_damage) -> bool:
        self.hp -= incoming_damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            return False
        else:
            return True

# name TEXT, b_mo TEXT, hp INTEGER, mp INTEGER, attack INTEGER, defense INTEGER, gold INTEGER, xp INTEGER
class Enemy(Actor):
    def __init__(self, name: str, b_mo: str, hp:int, mp:int, attack:int, defense:int, gold:int, exp:int):
        super().__init__(name, b_mo, hp, mp, attack, defense)
        self.name = name
        self.b_mo = b_mo
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.gold = gold
        self.exp = exp

    def is_alive(self) -> bool:
        if self.hp <= 0:
            return False
        else:
            return True


class Hero(Actor):
    # level INTEGER, hp INTEGER, mp INTEGER, attack INTEGER, defense INTEGER, req_xp INTEGER
    def __init__(self, name: str, b_mo: str, inventory: list, gold: int, exp: int,
                 level: int, hp: int, mp: int, attack: int, defense: int, req_xp: int):
        super().__init__(name, b_mo, hp, mp, attack, defense)
        self.level = level
        self.name = name
        self.birthday_month = b_mo
        self.hp = hp
        self.base_hp = hp
        self.mp = mp
        self.base_mp = mp
        self.attack = attack
        self.base_attack = attack
        self.defense = defense
        self.base_defense = defense
        self.inventory = inventory
        self.gold = gold
        self.exp = exp
        self.req_xp = req_xp

    def __str__(self):
        return f'Lvl:{self.level}\tName:{self.name}\tMonth:{self.birthday_month}\nHP:{self.hp}/{self.base_hp}\tMP:{self.mp}/{self.base_mp}\tATK:{self.attack}/{self.base_attack}\tDEF:{self.defense}/{self.base_defense}\nGil:{self.gold}\tXP:{self.exp}/{self.req_xp}'

    def __repr__(self):
        return f'{self.level},{self.name}, {self.birthday_month}, {self.hp}, {self.base_hp}, {self.mp}, {self.base_mp}, {self.attack}, {self.base_attack}, {self.defense}, {self.base_defense}, {self.inventory}, {self.gold}, {self.exp}, {self.req_xp}'

    def rest(self) -> None:
        self.hp = self.base_hp
        self.mp = self.base_mp
        self.alive = True

    def is_alive(self) -> bool:
        if self.hp <= 0:
            return False
        else:
            return True

    def equip_weapon(self, w: Equippable) -> None:
        self.hp += w.hp_mod
        self.mp += w.mp_mod
        self.attack += w.attack
        self.defense += w.defense
        print(f'You equipped a {w.name}!')
        print(f'You get + {w.hp_mod} HP!')
        print(f'You get + {w.mp_mod} MP!')
        print(f'You get + {w.attack} Attack!')
        print(f'You get + {w.defense} Defense!')

    def heal(self, incoming_hp) -> None:
        self.hp += incoming_hp
        if self.hp > self.base_hp:
            self.hp = self.base_hp

    def greet(self) -> str:
        return f'Hello {self.name}, \nwelcome to the world of your own imagination!I\'m happy you can be here, how lovely someone born in {self.birthday_month} could be so polite!'


class Game:
    def __init__(self, our_hero: Hero, database: DBSetup):
        self.our_hero = our_hero
        self.game_database = database

    def game_loop(self):
        while True:
            self.camp()

    def battle(self) -> None:
        # Beginning of Game loop
        our_enemy = Enemy(*self.game_database.new_enemy())
        battling = True
        confirm = input(f'You encountered an {our_enemy.name}')
        while battling:
            print(str(our_hero))
            print(f'You attack {our_enemy.name} for {our_hero.attack} Damage!')
            our_enemy.hp -= our_hero.attack
            if not our_enemy.is_alive():
                print(f'{our_enemy.name} was Defeated!')
                print(f'You gained {our_enemy.exp} XP!')
                our_hero.exp += our_enemy.exp
                print(f'You gained {our_enemy.gold} Gold!')
                our_hero.gold += our_enemy.gold
                break

            print(f'{our_enemy.name} attacks you for {our_enemy.attack} Damage!')
            our_hero.hp -= our_enemy.attack
            if not our_hero.is_alive():
                battling = False
                print(f'You were Defeated!')
                break

            confirm = input('Press Enter to continue')

    def camp(self) -> None:
        print('You Arrive at Camp, and are rested')
        self.our_hero.rest()
        next_place = choice('YOU ARE AT CAMP', ['Adventure', 'Blacksmith', 'Riddler', 'Save', 'Load'])
        if next_place == 1:
            print('you tried to adventure')
            self.adventure()
        elif next_place == 2:
            self.blacksmith()
        elif next_place == 3:
            self.merchant()
        elif next_place == 4:
            self.save()
        elif next_place == 5:
            self.load()

    # name: str, b_mo: str, inventory:list, level: int, hp:int, mp:int, attack:int, defense:int, gold:int,
    #                  exp:int, req_xp:int
    def levelup(self) -> str:
        self.our_hero = Hero(self.our_hero.name, self.our_hero.b_mo, self.our_hero.inventory, self.our_hero.gold, self.our_hero.exp
                             *self.game_database.actor_by_level(self.our_hero.level + 1))
        return str(self.our_hero)

    def adventure(self):
        print("You leave camp to adventure")
        ran_event_num = random.randrange(1, 100)
        if ran_event_num in range(1, 25):
            self.battle()
        elif ran_event_num in range(26, 50):
            self.battle()
        elif ran_event_num in range(51, 75):
            self.battle()
        elif ran_event_num in range(76, 100):
            self.riddler()

    def found_gear(self):
        print('You found some gear!')

    def riddler(self):
        print('You ran into the riddler...')

    def save(self):
        print('You gaze into to the Saving pool...')

    def load(self):
        print('You talk to the Loading pool...')

    def blacksmith(self):
        print('You talk to the blacksmith...')

    def merchant(self):
        print('You talk to the merchant...')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if os.path.exists('./db/game.db'):
        os.remove('./db/game.db')
    our_db = DBSetup()
    our_db.setupdb()

    # Credits Screen
    print('Welcome to MyRPG!\nColin Burke 2022!\nApril RPG Game Jam!\nLike and Subscribe!')

    # Get user's name
    user_name = input('Please enter your name, brave traveler!')

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']

    months_short = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct',
                    'nov', 'dec']

    month = ''
    # Get user's birthday month
    while month.lower() not in months and month.lower() not in months_short:
        month = str(input('Please type your birth month')).lower()
        if month.lower() not in months and month.lower() not in months_short:
            print('Not a valid month, try again')

    # *our_db.new_actor() =
    # level INTEGER, hp INTEGER, mp INTEGER, attack INTEGER, defense INTEGER, req_xp INTEGER)")
    print(*our_db.new_actor())
    our_hero = Hero(user_name, month, [], 0, 0, *our_db.new_actor())
    our_weapon = Equippable('Stick', 0, 5, 2, 0, 0, 24, 100)
    our_hero.equip_weapon(our_weapon)
    our_game = Game(our_hero, our_db)
    our_game.game_loop()

# Game loop
