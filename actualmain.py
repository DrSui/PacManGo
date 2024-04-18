import random
import json
from jsonFormatter import format
import time
import sys

def checkNoDuplicate(dict, x):
    for i in range(1,len(dict)+1):
        if dict[f"{i}"]["name"] == x:
            return False
    return True
class GeraldsStore:
    def __init__(self):
        with open("gerald.json","r") as f:
            data = json.load(f)
            self.money = data["money"]
            self.items = data["items"]
            f.close()
    def listItems(self):
        for i in range(len(self.items)):
            print(f"{i}: {self.items[f'{i}']['item']['name']}:  {self.items[f'{i}']['item']['description']} cost: {self.items[f'{i}']['price']}")
    def buyFrom(self, user):
        self.listItems() # this is pissing me off but "clean" code ig
        print(f"your money: {user.money}")
        u = input("enter the number you wish to buy")
        try:
            if user.money >= self.items[u]["price"] and checkNoDuplicate(user.attacks_disabled, self.items[u]["item"]["name"]):
                user.money -= self.items[u]["price"] 
                user.attacks_disabled[len(user.attacks_disabled)+1] = self.items[u]["item"]
                del self.items[u] # comment out if testing for ability to buy items , if file gone copy from gerald-ref BUT DO NOT use as main file
                self.saveFile()
                user.saveLiveUser()
                print("the fine print reads...  NO REFUNDS!!")
                user.changeAttacks()
            elif checkNoDuplicate(user.attacks_disabled, self.items[u]["item"]["name"]) == False:
                print("you already own this attack")
            else:
                print("you are too poor to afford this item and Gerald's General Store is a premiun establishment (you got kicked out for beign homeless")
        except Exception as e:
            print(e)
            print("you have failed to type a singhular nunmber.... Gerald kicked you out")
    def saveFile(self):
        with open("gerald.json", "w") as f:
            json.dump({"money": self.money, "items": self.items}, f)
            f.close()

class Character:
    def __init__(self, name, speed, stamina, strength, hp, attack, defence, attacks, money=0):
        self.money = money
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
                self.strength *= self.attack[attackIndex]["effect"][1]
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
    def __init__(self, name, speed, stamina, strength, hp, attack, defence, attacks, attacks_disabled, money):
        super().__init__(name, speed, stamina, strength, hp, attack, defence, attacks,money)
        self.attacks_disabled = attacks_disabled
    def getLiveUser():
        with open("user-live.json", "r") as f:
            d = json.load(f)
            f.close()
            return User(d["name"], d["speed"], d["stamina"], d["strength"], d["hp"], d["attack"], d["defence"], d["attacks"], d["attacks_disabled"], d["money"])
    def saveLiveUser(self):
        with open("user-live.json", "w") as f:
            tempDict = format(self.name, self.speed, self.stamina, self.strength, self.hp, self.attack, self.defence, self.attacks, self.attacks_disabled, self.money)
            json.dump(format(self.name, self.speed, self.stamina, self.strength, self.hp, self.attack, self.defence, self.attacks, self.attacks_disabled, self.money), f)
            f.close()
        print("user data saved")
    def level_up(self):
        # check if the user's hp is greater than 0 after defeating the enemy
        if self.hp > 0:
            # increase user's stats
            self.stamina += 2
            self.strength += 5
            self.speed = self.speed_original  # reset speed
            # reset hp
            self.hp += 20
            # return the next enemy to face
        else:
            return None
    def gym(self):
        u = int(input("enter wut u want to do (1) push (2) cardio (3) core (4) legs :( enter the number"))
        if u == 1:
            self.strength += 10
            for i in range(1,len(self.attacks)+1):
                self.attacks[i]["dmg"] += 2
            print("you've improved your strength and increased the damage of all your attacks!")
        elif u == 2:
            self.stamina += 10
            print("you've improved your stamina and increased the rate of dodging!")
        elif u == 3:
            self.hp += 5
            print("you've improved your hp!")
        elif u == 4:
            self.speed += 5
            print("You've improved your speed!")
    def changeAttacks(self):
        print("current attacks:")
        for i in range(1,len(self.attacks)+1):
            print(f"({i}). {self.attacks[f'{i}']['name']} - {self.attacks[f'{i}']['description']}")
        print("not selected attacks:")
        for i in range(1,len(self.attacks_disabled)+1):
            print(f"({i}). {self.attacks_disabled[f'{i}']['name']} - {self.attacks_disabled[f'{i}']['description']}")
        u = input("enter the number associated with the attack you wish to swap out and the attack you want to replace it seperated by spaces i.e. 1 0")
        a,b = u.split(" ")
        try:
            self.attacks[a] , self.attacks_disabled[b] = self.attacks_disabled[b], self.attacks[a]
            print("swapped succesfully")
        except(e):
            print("error , follow the correct format")
    def attackLoop(self, enemy):
        while self.hp > 0 and enemy.hp > 0:
            print(f"{enemy.name} has {enemy.hp} HP.")
            print(f"{self.name} has {self.hp} HP.")
            for i in range(1,len(self.attacks)+1):
                print(f"({i}). {self.attacks[f'{i}']['name']} - {self.attacks[f'{i}']['dmg']}")
            u = int(input("enter the attack number you want to use"))
            # Determine who goes first based on speed
            if enemy.speed >= self.speed:
                print("The enemy has the initiative and goes first!")
                enemy.attackEnemy(self, str(random.randint(1,len(enemy.attacks))))
                if user.hp > 0:
                    user.attackEnemy(enemy,str(u))
            else:
                print("You have the initiative and go first!")
                self.attackEnemy(enemy, str(u))
                if enemy.hp > 0:
                    enemy.attackEnemy(user, str(random.randint(1,len(enemy.attacks))))
        self = User.getLiveUser()
        return self.hp > enemy.hp 
def reset_enemies():
    with open("enemies-attacks.json","r") as f:
        data = json.load(f)
        MRpriestley = Character("MrPriestley",10,12,50,100,30,30,data["MrPriestley"])
        MRbrown = Character("MrBrown",12,15,60,100,35,25,data["MrBrown"])
        MrSmith = Character("MrSmith",30,30,100,100,100,210,data["MrSmith"])

        return [MRpriestley,MRbrown, MrSmith]###mrsmith added

def create_new_user():
    name = input("Enter the name for your character: ")
    # default attacks probably change soon 
    attacks = {
        "1": {"name": "jab", "description": "its a jab", "type": "basic", "dmg": 50},
        "2": {"name": "cross", "description": "its a jab but sideways", "type": "basic", "dmg": 12},
        "3": {"name": "hook", "description": "its a jab but sideways the quick way", "type": "basic", "dmg": 12},
        "4": {"name": "body shot", "description": "its a jab but low", "type": "basic", "dmg": 14},

    }
    attacks_disabled = { 
        "1": {"name": "uppercut", "description": "its a jab but vertical", "type": "basic", "dmg": 18},
              "2": {"name": "dodge", "description": "you dodge", "type": "dodge", "dmg": 0}
    }
    user = User(name, 11, 13, 100, 100, 10, 10, attacks, attacks_disabled, 10000) # reset attacks to live version of user
    user.saveLiveUser()
    return user

def combat_execution(user):
    # MRsmith = Character()
    gerald = GeraldsStore()
    print("me to the combat game!")
    user = User.getLiveUser()
    print("Press Enter to start...")
    input()
    print("User Status:")
    print(f"Speed: {user.speed}")
    print(f"Stamina: {user.stamina}")
    print(f"Strength: {user.strength}")
    print(f"HP: {user.hp}")
    while True: # main loop
        match input("enter what you want to do 1. visit Gerald's General Store 2. fight some people from the local turkish barbers 3. boss fight"):
            case "1":
                option = 1
                break
            case "2":
                option = 2
                break
            case "3":
                option = 3
                break
            case _:
                print("learn to type")
   # user.changeAttacks() #  debugging only
    while True:
        if option == 1:
            #print("work in progress... Gerald's General Store is under construction")
            #combat_execution(user)
            gerald.buyFrom(user)
            print(user.attacks_disabled)
        elif option == 2:
            print("its eid all the turkish barbers are closed...")
            combat_execution(user)
            break
        elif option == 3:
            pass
        enemies = reset_enemies()
        
        for index in range(len(enemies)):
            user.saveLiveUser()
            print(index)
            enemy = enemies[index]
            print(len(enemy.attacks))
            print(enemy.attacks[str(1)])
            print(f"You are facing an enemy with {enemy.hp} HP.")
            won = user.attackLoop(enemy)
            if user.hp > 0:
                user = User.getLiveUser()
                user.level_up()
                if index<len(enemies)-1:
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

        restart_game = input("Do you want to start a new game? (yes/no)").lower()
        if restart_game == "no":
            break

if __name__ == "__main__":
    global user
    user = create_new_user()
    combat_execution(user)
