def format(name, speed, stamina, strength, hp, attack, defence, attacks, attacks_disabled):
    character_data = {
        "name": name,
        "speed": speed,
        "stamina": stamina,
        "strength": strength,
        "hp": hp,
        "attack": attack,
        "defence": defence,
        "attacks": attacks,
        "attacks_disabled": attacks_disabled
    }
    return character_data
