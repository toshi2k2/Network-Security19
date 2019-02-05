import sys
import random

class EscapeRoom:

    def start(self):
        '''This method initializes the game'''
        self.time = 100
        self.on_glasses = False
        self.stat = 'locked'
        self.inventory = []
        self.pin = True  # hairpin is in hair
        self.floor = False  # haven't looked at the floor
        self.mirror = False  # haven't looked into the mirror
        self.hammer = False  # haven't got hammer
        self.glasses = False  # haven't got glasses
        self.open_chest = False  # chest ain't open
        self.open_board = False  # board ain't open
        self.unlock_chest = False
        self.code = random.randint(0, 9999)
        self.unlock_door = False  # door is locked
        self.open_door = False  # door is not open

        self.string_code = str(self.code)

    def command(self, command_string):
        '''This command accepts the user's command within the game'''

        self.time -= 1
        commandParts = command_string.split(" ")

        while len(self.string_code) < 4:
            self.string_code = '0' + self.string_code

        def look(cp):
            if len(cp) == 1:
                return "You are in a locked room. There is only one door" \
                       "\nand it has a numeric keypad. Above the door is a clock that reads {}." \
                       "\nAcross from the door is a large mirror. Below the mirror is an old chest." \
                       "\n\nThe room is old and musty and the floor is creaky and warped.".format(self.time)

            elif len(cp) == 2:

                if cp[1] == 'door' and not self.on_glasses:
                    return "The door is strong and highly secured. The door is locked and requires a 4-digit code to open."
                elif cp[1] == 'door' and self.on_glasses:
                    return "The door is strong and highly secured. The door is locked and requires a 4-digit code " \
                           "to open. But now you're wearing these glasses you notice something! " \
                           "There are smudges on the digits {}.".format(",".join(sorted(set(self.string_code))))

                elif cp[1] == 'mirror' and not self.pin:  # hairpin not in hair
                    self.mirror = True
                    return "You look in the mirror and see yourself."
                elif cp[1] == 'mirror' and self.pin:
                    self.mirror = True
                    return "You look in the mirror and see yourself... wait, there's a hairpin in your hair. " \
                           "Where did that come from?"

                elif cp[1] == 'chest':
                    return "An old chest. It looks worn, but it's still sturdy."

                elif cp[1] == 'floor':
                    self.floor = True
                    return "The floor makes you nervous. It feels like it could fall in. One of the boards is loose."

                elif cp[1] == 'board' and not self.floor:
                    return "You don't see that here."
                elif cp[1] == 'board' and not self.open_board:
                    return "The board is loose, but won't come up when you pull on it. " \
                           "Maybe if you pried it open with something."
                elif cp[1] == 'board' and self.open_board:
                    return "The board has been pulled open. You can look inside."

                elif cp[1] == 'hairpin' and not self.mirror:
                    return "You don't see that here."
                elif cp[1] == 'hairpin' and self.mirror:
                    return "You see nothing special."

                elif cp[1] == 'hammer' and not self.hammer:
                    return "You don't see that here."
                elif cp[1] == 'hammer' and self.hammer:
                    return "You see nothing special."

                elif cp[1] == 'glasses' and 'glasses' not in self.inventory:
                    return "You don't see that here."
                elif cp[1] == 'glasses' and 'glasses' in self.inventory:
                    return "These look like spy glasses. Maybe they reveal a clue!"

                elif cp[1] == 'clock':
                    return "You see nothing special."

                else:
                    return "You don't see that here."

            elif cp[1] == 'in' and len(cp) == 3:
                if cp[2] == 'chest' and not self.hammer and self.open_chest:
                    return "Inside the chest you see: a hammer."
                elif cp[2] == 'chest' and self.hammer:
                    return "Inside the chest you see: ."
                elif cp[2] == 'chest' and self.hammer and not self.open_chest:
                    return "Its not open!"  # need to change this !

                elif cp[2] == 'board' and not self.glasses:
                    return "Inside the board you see: a glasses."
                elif cp[2] == 'board' and self.glasses:
                    return "Inside the board you see: ."
                elif cp[2] == 'board' and not self.open_board:
                    return "Although loose, you can't look in the board until it's pried open."

                else:
                    return "You can't look in that!"

            else:
                return "You can't do that."

        def wear(cp):
            if cp[1] == 'glasses':
                if not self.on_glasses:
                    if 'glasses' in self.inventory:  # write an inv list
                        self.on_glasses = True
                        return "You are now wearing the glasses."
                    else:
                        return "You don't have a glasses."
                elif self.on_glasses:
                    return "You're already wearing them!"
            elif len(cp) == 2:
                return "You don't have a {}.".format(cp[1])
            else:
                return "You can't do that."

        def get(cp):
            if len(cp) == 2:  # get <object>
                if cp[1] == 'hairpin' and not self.mirror:
                    return "You don't see that."
                elif cp[1] == 'hairpin' and self.mirror and 'hairpin' not in self.inventory:
                    self.inventory.append('hairpin')
                    self.pin = False
                    return "You got it."
                elif cp[1] == 'hairpin' and 'hairpin' in self.inventory:
                    return "You already have that."

                elif cp[1] == 'board' and not self.floor:
                    return "You don't see that."
                elif cp[1] == 'board' and self.floor:
                    return "You can't get that."

                elif cp[1] == 'door' or 'clock' or 'mirror' or 'chest' or 'floor':
                    return "You can't get that."

                elif cp[1] == 'hammer' and 'hammer' in self.inventory:
                    return "You already have that."

                elif cp[1] == 'glasses' and 'glasses' in self.inventory:
                    return "You already have that."

                else:
                    return "You don't see that."

            if len(cp) > 2 and cp[2] == 'from':
                if cp[1] == 'hammer' and cp[3] == 'chest' and not self.open_chest:
                    return "It's not open."
                elif cp[1] == 'hammer' and cp[3] == 'chest' and self.open_chest and not self.hammer:
                    self.hammer = True
                    self.inventory.append('hammer')
                    return "You got it."
                elif cp[1] == 'hammer' and cp[3] == 'chest' and self.open_chest and self.hammer:
                    return "You don't see that."

                elif cp[1] == 'glasses' and cp[3] == 'board' and not self.open_board:
                    return "It's not open."
                elif cp[1] == 'glasses' and cp[3] == 'board' and self.open_board and 'glasses' not in self.inventory:
                    self.inventory.append('glasses')
                    return "You got it."
                elif cp[1] == 'glasses' and cp[3] == 'board' and self.open_board and 'glasses' in self.inventory:
                    return "You don't see that."

                else:
                    return "You can't get something out of that!"

        def inventory():
            inv = ["a {}".format(object) for object in self.inventory]
            out_inv = ", ".join(inv)
            return "You are carrying {}.".format(out_inv)

        def unlock(cp):
            if cp[1] == 'chest':
                if len(cp) > 2 and cp[2] == 'with':
                    if cp[3] == 'hairpin' and 'hairpin' in self.inventory and self.unlock_chest:
                        return "It's already unlocked."
                    elif cp[3] == 'hairpin' and 'hairpin' in self.inventory and not self.unlock_chest:
                        self.unlock_chest = True
                        return "You hear a click! It worked!"
                    elif cp[3] != 'hairpin':
                        return "You don't have a {}.".format(cp[3])
                    else:
                        return "you can't do that."
                else:
                    return "You can't do that."

            elif cp[1] == 'door' and self.unlock_door:  # check this!
                return "It's already unlocked."
            elif cp[1] == 'door' and cp[2] == 'with':
                if len(cp[3]) < 4:
                    return "The code must be 4 digits."
                elif not cp[3].isdigit():
                    return "That's not a valid code."
                elif cp[3] == self.string_code and not self.unlock_door:
                    self.unlock_door = True
                    return "You hear a click! It worked!"
                elif cp[3] != self.string_code:
                    return "That's not the right code!"

            elif cp[3] == 'hairpin' and not self.mirror:
                return "You don't see that here."

            elif cp[3] == 'board' and not self.floor:
                return "You don't see that here."

            elif cp[3] == 'hammer' and 'hammer' not in self.inventory:
                return "You don't see that here."

            elif cp[3] == 'glasses' and 'glasses' not in self.inventory:
                return "You don't see that here."

            elif cp[1] in [clock, mirror, hairpin, floor, board, hammer, glasses]:
                return "You can't unlock that!"

            else:
                return "You don't see that here."

        def open(cp):
            if cp[1] == 'chest':
                if not self.unlock_chest:
                    return "It's locked."
                elif self.unlock_chest and not self.open_chest:
                    self.open_chest = True
                    return "You open the chest."
                elif self.open_chest:
                    return "It's already open!"
                else:
                    return "You can't do that."

            elif cp[1] == 'door':
                if not self.unlock_door:
                    return "It's locked."
                elif self.unlock_door and not self.open_door:
                    self.open_door = True
                    if self.time != 0:
                        self.stat = "escaped"
                    return "You open the door."

            elif cp[1] == 'hairpin' and not self.mirror:
                return "You don't see that."

            elif cp[1] == 'board' and not self.floor:
                return "You don't see that."

            elif cp[1] == 'hammer' and 'hammer' not in self.inventory:
                return "You don't see that."

            elif cp[1] == 'glasses' and 'glasses' not in self.inventory:
                return "You don't see that."

            elif cp[1] in [clock, mirror, hairpin, floor, board, hammer, glasses]:
                return "You can't open that!"

            else:
                return "You don't see that."

        def pry(cp):
            if cp[1] == 'board' and self.open_board:
                return "It's already pried open."
            elif cp[1] == 'board' and cp[2] == 'with':
                if not self.floor:
                    return "You don't see that."
                elif cp[3] == 'hammer' and 'hammer' not in self.inventory:
                    return "You don't have a hammer."
                elif cp[3] == 'hammer' and 'hammer' in self.inventory:
                    self.open_board = True
                    return "You use the hammer to pry open the board. It takes some work, but with " \
                           "some blood and sweat, you manage to get it open."
                elif cp[3] != 'hammer' and cp[3] in self.inventory:
                    return "Don't be stupid! That won't work!"
                else:
                    return "You don't have a {}.".format(cp[3])

            elif cp[1] == 'hairpin' and cp[2] == 'with' and not self.mirror:
                return "You don't see that."

            elif cp[1] == 'hammer' and cp[2] == 'with' and 'hammer' not in self.inventory:
                return "You don't see that."

            elif cp[1] == 'glasses' and cp[2] == 'with' and 'glasses' not in self.inventory:
                return "You don't see that."

            elif cp[1] in [door, clock, mirror, hairpin, chest, floor, hammer, glasses]:
                return "Don't be stupid! That won't work!"

            else:
                return "You don't see that."

        if commandParts[0] == 'look':
            out = look(commandParts)
        elif commandParts[0] == 'get':
            out = get(commandParts)
        elif commandParts[0] == 'inventory':
            out = inventory()
        elif commandParts[0] == 'unlock':
            out = unlock(commandParts)
        elif commandParts[0] == 'open':
            out = open(commandParts)
        elif commandParts[0] == 'pry':
            out = pry(commandParts)
        elif commandParts[0] == 'wear':
            out = wear(commandParts)
        else:
            out = "You can't do that."

        if self.time == 0:
            self.stat = 'dead'
            out = out + "\nOh no! The clock starts ringing!!! After a few seconds, the room fills with a deadly " \
                        "gas..."
        return out

    def status(self):
        '''Reports whether the users is "dead", "locked", or "escaped"'''
        return self.stat


def main():
    room = EscapeRoom()
    room.start()
    while room.status() == "locked":
        command = input(">> ")
        # room.command(command)
        output = room.command(command)
        print(output)
    if room.status() == "escaped":
        # print("You escaped!")
        sys.exit()
    else:
        # print("You died!")
        sys.exit()

if __name__ == "__main__":
    main()