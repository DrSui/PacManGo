import random
import json
from jsonFormatter import format  # Assuming you have this formatter

class Character:
    def __init__(self, name, speed, stamina, strength, hp, attack, defence, attacks):
        self.name = name
        self.speed = speed
        self.speed_original = speed  # Store original speed for combat system reset
        self.stamina = stamina
        self.strength = strength
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.dodge_count = 0
        self.attacks = attacks

    def attackEnemy(self, enemy, attackIndex):
        attackType = self.attacks[attackIndex]["type"]

        if attackType == "buff":
            effect = self.attacks[attackIndex]["effect"][0]
            if effect == "speed":
                self.speed *= self.attacks[attackIndex]["effect"][1]
            elif effect == "strength":
                self.strength *= self.attacks[attackIndex]["effect"][1]
            # add more if needed
        elif attackType == "debuff":
            effect = self.attacks[attackIndex]["effect"][0]
            if effect == "speed":
                enemy.speed *= self.attacks[attackIndex]["effect"][1]
            elif effect == "strength":
                enemy.strength *= self.attack[attackIndex]["effect"][1]
        elif attackType == "dodge":
            if self.speed >= 10 and self.dodge_count < 2:
                self.hp += 20  # Restore health by 20
                self.dodge_count += 1
                print("You dodged the enemy's attack and restored your health!")
            else:
                print("You don't have enough speed to dodge or you've already dodged twice in this battle.")
            return

        print(f"{self.name} uses {self.attacks[attackIndex]['name']}! {self.attacks[attackIndex]['description']}")
        enemy.hp -= self.attacks[attackIndex]["dmg"]


class User(Character):
    def __init__(self, name, speed, stamina, strength, hp, attack, defence, attacks, attacks_disabled):
        super().__init__(name, speed, stamina, strength, hp, attack, defence, attacks)
        self.attacks_disabled = attacks_disabled

    @staticmethod
    def getLiveUser():
        with open("user-live.json", "r") as f:
            d = json.load(f)
            return User(d["name"], d["speed"], d["stamina"], d["strength"], d["hp"], d["attack"], d["defence"], d["attacks"], d["attacks_disabled"])

    def saveLiveUser(self):
        with open("user-live.json", "w") as f:
            tempDict = format(self.name, self.speed, self.stamina, self.strength, self.hp, self.attack, self.defence, self.attacks, self.attacks_disabled)
            json.dump(tempDict, f)
        print("user data saved")

    def level_up(self):
        # Check if the user's HP is greater than 0 after defeating the enemy
        if self.hp > 0:
            # Increase user's stats
            self.stamina += 2
            self.strength += 5
            self.speed = self.speed_original  # Reset speed
            # Reset HP
            self.hp += 20
            # Return the next enemy to face
        else:
            return None

    def gym(self):
        while True:
            try:
                u = int(input("Enter the activity you want to do (1: push, 2: cardio, 3: core, 4: legs): "))
                if u not in [1, 2, 3, 4]:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")

        if u == 1:
            self.strength += 10
            for i in range(1, len(self.attacks) + 1):
                self.attacks[i]["dmg"] += 2
            print("You've improved your strength and increased the damage of all your attacks!")
        elif u == 2:
            self.stamina += 10
            print("You've improved your stamina and increased the rate of dodging!")
        elif u == 3:
            self.hp += 5
            print("You've improved your HP!")
        elif u == 4:
            self.speed += 5
            print("You've improved your speed!")


def reset_enemies():
    with open("enemies-attacks.json", "r") as f:
        data = json.load(f)
        MRpriestley = Character("MrPriestley", 10, 12, 50, 100, 30, 30, data["MrPriestley"])
        MRbrown = Character("MrBrown", 12, 15, 60, 100, 35, 25, data["MrBrown"])
        return [MRpriestley, MRbrown]


def create_new_user():
    name = input("Enter the name for your character: ")
    attacks = {
        "1": {"name": "jab", "description": "its a jab", "type": "basic", "dmg": 50},
        "2": {"name": "cross", "description": "its a jab but sideways", "type": "basic", "dmg": 12},
        "3": {"name": "hook", "description": "its a jab but sideways the quick way", "type": "basic", "dmg": 12},
        "4": {"name": "body shot", "description": "its a jab but low", "type": "basic", "dmg": 14},
    }
    attacks_disabled = {
        "1": {"name": "uppercut", "description": "its a jab but vertical", "type": "basic", "dmg": 18},
        "2": {"name": "dodge", "type": "dodge", "dmg": 0}
    }
    user = User(name, 11, 13, 100, 100, 10, 10, attacks, attacks_disabled)
    user.saveLiveUser()
    return user


def combat_execution(user):
    print("Welcome to the combat game!")
    user = User.getLiveUser()
    print("Press Enter to start the battle...")
    input()
    print("User Status:")
    print(f"Speed: {user.speed}")
    print(f"Stamina: {user.stamina}")
    print(f"Strength: {user.strength}")
    print(f"HP: {user.hp}")
    print()

    while True:
        enemies = reset_enemies()
        for index, enemy in enumerate(enemies):
            user.saveLiveUser()
            print(f"You are facing an enemy with {enemy.hp} HP.")
            while user.hp > 0 and enemy.hp > 0:
                print(f"{enemy.name} has {enemy.hp} HP.")
                print(f"{user.name} has {user.hp} HP.")
                for i in range(1, len(user.attacks) + 1):
                    print(f"({i}). {user.attacks[f'{i}']['name']} - {user.attacks[f'{i}']['dmg']}")
                while True:
                    try:
                        u = int(input("Enter the attack number you want to use: "))
                        if u not in range(1, len(user.attacks) + 1):
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number corresponding to your attack.")

                # Determine who goes first based on speed
                if enemy.speed >= user.speed:
                    print("The enemy has the initiative and goes first!")
                    enemy.attackEnemy(user, str(random.randint(1, len(enemy.attacks))))
                    if user.hp > 0:
                        user.attackEnemy(enemy, str(u))
                else:
                    print("You have the initiative and go first!")
                    user.attackEnemy(enemy, str(u))
                    if enemy.hp > 0:
                        enemy.attackEnemy(user, str(random.randint(1, len(enemy.attacks))))


            if user.hp > 0:
                user = User.getLiveUser()
                user.level_up()
                if index < len(enemies) - 1:
                    print(f"You have leveled up to face {enemies[index+1].name}!")
                else:
                    print("Congratulations! You defeated all enemies and completed the game!")
                    break
            else:
                user = user.getLiveUser()
                print("You were defeated.")
                choice = input("Would you like to battle again or train at the gym? (battle/train/end): ").lower()
                if choice == "battle":
                    break
                elif choice == "train":
                    while True:
                        user.gym()
                        continue_training = input("Do you want to continue training? (yes/no): ").lower()
                        if continue_training == "no":
                            break
                        else:
                            print("Invalid exercise choice.")
                    break
                elif choice == "end":
                    return

        restart_game = input("Do you want to start a new game? (yes/no): ").lower()
        if restart_game == "no":
            break


if __name__ == "__main__":
    user = create_new_user()
    combat_execution(user)