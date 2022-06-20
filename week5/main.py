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
        c = input(('Your choice:'))
        if c.lower() in ('i', 'p'):
            return c
        c = int(c) - 1
    # if not within valid results, return first result
    except (ValueError, TypeError):
        c = 0
    if c not in range(1, len(ls) + 1) or c == 0:
        c = 0
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


class Enemy(Actor):
    def __init__(self, name: str, b_mo: str, hp=20, mp=5, attack=3, defense=2, gold=0, exp=0):
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
    def __init__(self, level: int, name: str, b_mo: str, hp=20, mp=0, attack=0, defense=0, inventory=None, gold=0,
                 exp=0, req_xp=0):
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
        if inventory is None:
            inventory = []
        self.inventory = inventory
        self.gold = gold
        self.exp = exp
        self.req_xp = req_xp

    def __str__(self):
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

    def battle(self, mob: Enemy) -> None:
        # Beginning of Game loop
        our_enemy = Enemy('Feisty Goblin', hp=60, b_mo='June')
        battling = True
        confirm = input(f'You encountered an {our_enemy.name}')
        while battling:
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
        next_place = choice('YOU ARE AT CAMP', ['Adventure', 'Save', 'Load', 'Blacksmith', 'Riddler'])

    def levelup(self) -> str:
        self.our_hero = Hero(self.our_hero.level + 1, self.our_hero.name, self.our_hero.b_mo,
                             *self.game_database.new_actor(self.our_hero.level + 1))
        return str(self.our_hero)

    def adventure(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def blacksmith(self):
        pass

    def riddler(self):
        pass


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
    while month not in months:
        month = str(input('Please type your birth month')).lower()
        if month not in months:
            print('Not a valid month, try again')

    starting_level = 1

    our_hero = Hero(starting_level, user_name, month, *our_db.new_actor(starting_level))
    print(our_hero)
    our_weapon = Equippable('Stick', 0, 5, 2, 0, 0, 24, 100)
    our_hero.equip_weapon(our_weapon)
    our_game = Game(our_hero, our_db)
    print(our_game.levelup())

# Game loop
