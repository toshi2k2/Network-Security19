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

    def command(self, command_string):
        '''This command accepts the user's command within the game'''

        self.time -= 1
        commandParts = command_string.split(" ")

        def look(cp):
            if len(cp) == 1:  # add time functionality
                print("You are in a locked room. There is only one door "
                      "and it has a numeric keypad. Above the door is a clock that reads {}. "
                      "\nAcross from the door is a large mirror. Below the mirror is an old chest."
                      "\n"
                      "\nThe room is old and musty and the floor is creaky and warped.".format(self.time))

            elif len(cp) == 2:

                if cp[1] == 'door' and not self.on_glasses:
                    print("The door is strong and highly secured. The door is locked and requires a 4-digit code to "
                          "open.")
                elif cp[1] == 'door' and self.on_glasses:
                    print("The door is strong and highly secured. The door is locked and requires a 4-digit code "
                          "to open. But now you're wearing these glasses you notice something! "
                          "There are smudges on the digits {}.".format(",".join(sorted(str(self.code)))))

                elif cp[1] == 'mirror' and not self.pin:  # hairpin not in hair
                    print("You look in the mirror and see yourself.")
                    self.mirror = True
                elif cp[1] == 'mirror' and self.pin:
                    print("You look in the mirror and see yourself... wait, there's a hairpin in your hair. "
                          "Where did that come from?")
                    self.mirror = True

                elif cp[1] == 'chest':
                    print("An old chest. It looks worn, but it's still sturdy.")

                elif cp[1] == 'floor':
                    print("The floor makes you nervous. It feels like it could fall in. One of the boards is loose.")
                    self.floor = True

                elif cp[1] == 'board' and not self.floor:
                    print("You don't see that here.")
                elif cp[1] == 'board' and not self.open_board:
                    print("The board is loose, but won't come up when you pull on it. "
                          "Maybe if you pried it open with something.")
                elif cp[1] == 'board' and self.open_board:
                    print("The board has been pulled open. You can look inside.")

                elif cp[1] == 'hairpin' and not self.mirror:
                    print("You don't see that here.")
                elif cp[1] == 'hairpin' and self.mirror:
                    print("You see nothing special.")

                elif cp[1] == 'hammer' and not self.hammer:
                    print("You don't see that here.")
                elif cp[1] == 'hammer' and self.hammer:
                    print("You see nothing special.")

                elif cp[1] == 'glasses' and 'glasses' not in self.inventory:
                    print("You don't see that here.")
                elif cp[1] == 'glasses' and 'glasses' in self.inventory:
                    print("These look like spy glasses. Maybe they reveal a clue!")

                elif cp[1] == 'clock':
                    print("You see nothing special.")

                else:
                    print("You don't see that here.")

            elif cp[1] == 'in' and len(cp) == 3:
                if cp[2] == 'chest' and not self.hammer and self.open_chest:
                    print("Inside the chest you see: a hammer.")
                elif cp[2] == 'chest' and self.hammer:
                    print("Inside the chest you see: .")
                elif cp[2] == 'chest' and self.hammer and not self.open_chest:
                    print("Its not open!")  # need to change this !

                elif cp[2] == 'board' and not self.glasses:
                    print("Inside the board you see: a glasses.")
                elif cp[2] == 'board' and self.glasses:
                    print("Inside the board you see: .")

                else:
                    print("You can't look in that!")

            else:
                print("You can't do that.")

        def wear(cp):
            if cp[1] == 'glasses':
                if not self.on_glasses:
                    if 'glasses' in self.inventory:  # write an inv list
                        print("You are now wearing the glasses.")
                        self.on_glasses = True
                    else:
                        print("You don't have a glasses.")
                elif self.on_glasses:
                    print("You're already wearing them!")
            elif len(cp) == 2:
                print("You don't have a {}.".format(cp[1]))
            else:
                print("You can't do that.")

        def get(cp):
            if len(cp) == 2:  # get <object>
                if cp[1] == 'hairpin' and not self.mirror:
                    print("You don't see that.")
                elif cp[1] == 'hairpin' and self.mirror and 'hairpin' not in self.inventory:
                    print("You got it.")
                    self.inventory.append('hairpin')
                    self.pin = False
                elif cp[1] == 'hairpin' and 'hairpin' in self.inventory:
                    print("You already have that.")

                elif cp[1] == 'board' and not self.floor:
                    print("You don't see that.")
                elif cp[1] == 'board' and self.floor:
                    print("You can't get that.")

                elif cp[1] == 'door' or 'clock' or 'mirror' or 'chest' or 'floor':
                    print("You can't get that.")

                elif cp[1] == 'hammer' and 'hammer' in self.inventory:
                    print("You already have that.")

                elif cp[1] == 'glasses' and 'glasses' in self.inventory:
                    print("You already have that.")

                else:
                    print("You don't see that.")

            if len(cp) > 2 and cp[2] == 'from':
                if cp[1] == 'hammer' and cp[3] == 'chest' and not self.open_chest:
                    print("It's not open.")
                elif cp[1] == 'hammer' and cp[3] == 'chest' and self.open_chest and not self.hammer:
                    print("You got it.")
                    self.hammer = True
                    self.inventory.append('hammer')
                elif cp[1] == 'hammer' and cp[3] == 'chest' and self.open_chest and self.hammer:
                    print("You don't see that.")

                elif cp[1] == 'glasses' and cp[3] == 'board' and not self.open_board:
                    print("It's not open.")
                elif cp[1] == 'glasses' and cp[3] == 'board' and self.open_board and 'glasses' not in self.inventory:
                    print("You got it.")
                    self.inventory.append('glasses')
                elif cp[1] == 'glasses' and cp[3] == 'board' and self.open_board and 'glasses' in self.inventory:
                    print("You don't see that.")

        def inventory():
            inv = ["a {}".format(object) for object in self.inventory]
            out_inv = ", ".join(inv)
            print("You are carrying {}.".format(out_inv))

        def unlock(cp):
            if cp[1] == 'chest':
                if len(cp) > 2 and cp[2] == 'with':
                    if cp[3] == 'hairpin' and 'hairpin' in self.inventory and self.unlock_chest:
                        print("It's already unlocked.")
                    elif cp[3] == 'hairpin' and 'hairpin' in self.inventory and not self.unlock_chest:
                        print("You hear a click! It worked!")
                        self.unlock_chest = True
                    elif cp[3] != 'hairpin':
                        print("You don't have a {}.".format(cp[3]))
                    else:
                        print("you can't do that.")
                else:
                    print("You can't do that.")

            elif cp[1] == 'door' and self.unlock_door:  # check this!
                print("It's already unlocked.")
            elif cp[1] == 'door' and cp[2] == 'with':
                if len(cp[3]) < 4:
                    print("The code must be 4 digits.")
                elif not cp[3].isdigit():
                    print("That's not a valid code.")
                elif int(cp[3]) == self.code and not self.unlock_door:
                    print("You hear a click! It worked!")
                    self.unlock_door = True
                elif int(cp[3]) != self.code:
                    print("That's not the right code!")

            elif cp[3] == 'hairpin' and not self.mirror:
                print("You don't see that here.")

            elif cp[3] == 'board' and not self.floor:
                print("You don't see that here.")

            elif cp[3] == 'hammer' and 'hammer' not in self.inventory:
                print("You don't see that here.")

            elif cp[3] == 'glasses' and 'glasses' not in self.inventory:
                print("You don't see that here.")

            elif cp[1] in [clock, mirror, hairpin, floor, board, hammer, glasses]:
                print("You can't unlock that!")

            else:
                print("You don't see that here.")

        def open(cp):
            if cp[1] == 'chest':
                if not self.unlock_chest:
                    print("It's locked.")
                elif self.unlock_chest and not self.open_chest:  #write unlock function
                    print("You open the chest.")
                    self.open_chest = True
                elif self.open_chest:
                    print("It's already open!")
                else:
                    print("You can't do that.")

            elif cp[1] == 'door':
                if not self.unlock_door:
                    print("It's locked.")
                elif self.unlock_door and not self.open_door:
                    print("You open the door.")
                    self.open_door = True
                    if self.time != 0:
                        self.stat = "escaped"

            elif cp[1] == 'hairpin' and not self.mirror:
                print("You don't see that.")

            elif cp[1] == 'board' and not self.floor:
                print("You don't see that.")

            elif cp[1] == 'hammer' and 'hammer' not in self.inventory:
                print("You don't see that.")

            elif cp[1] == 'glasses' and 'glasses' not in self.inventory:
                print("You don't see that.")

            elif cp[1] in [clock, mirror, hairpin, floor, board, hammer, glasses]:
                print("You can't open that!")

            else:
                print("You don't see that.")

        def pry(cp):
            if cp[1] == 'board' and self.open_board:
                print("It's already pried open.")
            elif cp[1] == 'board' and cp[2] == 'with':
                if not self.floor:
                    print("You don't see that.")
                elif cp[3] == 'hammer' and 'hammer' not in self.inventory:
                    print("You don't have a hammer.")
                elif cp[3] == 'hammer' and 'hammer' in self.inventory:
                    print("You use the hammer to pry open the board. It takes some work, but with "
                          "some blood and sweat, you mange to get it open.")
                    self.open_board = True
                else:
                    print("You don't have a {}.".format(cp[3]))

            elif cp[1] == 'hairpin' and cp[2] == 'with' and not self.mirror:
                print("You don't see that.")

            elif cp[1] == 'hammer' and cp[2] == 'with' and 'hammer' not in self.inventory:
                print("You don't see that.")

            elif cp[1] == 'glasses' and cp[2] == 'with' and 'glasses' not in self.inventory:
                print("You don't see that.")

            elif cp[1] in [door, clock, mirror, hairpin, chest, floor, hammer, glasses]:
                print("Don't be stupid! That won't work!")

            else:
                print("You don't see that.")

        if commandParts[0] == 'look':
            look(commandParts)
        elif commandParts[0] == 'get':
            get(commandParts)
        elif commandParts[0] == 'inventory':
            inventory()
        elif commandParts[0] == 'unlock':
            unlock(commandParts)
        elif commandParts[0] == 'open':
            open(commandParts)
        elif commandParts[0] == 'pry':
            pry(commandParts)
        elif commandParts[0] == 'wear':
            wear(commandParts)
        else:
            print("You can't do that.")

        if self.time == 0:
            print("Oh no! The clock starts ringing!!! After a few seconds, the room fills with a deadly gas...")
            self.stat = 'dead'
            # status()

        # if self.stat == 'dead':
        #     sys.exit()
        # if self.stat == 'escaped':
        #     sys.exit()

    def status(self):
        '''Reports whether the users is "dead", "locked", or "escaped"'''
        return self.stat


def main():
    room = EscapeRoom()
    room.start()
    while room.status() == "locked":
        command = input(">> ")
        room.command(command)
        # output = room.command(command)
        # print(output)
    if room.status() == "escaped":
        print("Congratulations! You escaped!")
    else:
        print("Sorry. You died.")

if __name__ == "__main__":
    main()