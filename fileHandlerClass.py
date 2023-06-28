import pygame


'''this class is used to handle the file "keys.txt" which contains the current keyboard keys that the player chooses
in setting class. the keys are read in game initialization so the player can choose to change keys as he see fits.
it is used by gameManage class and settings class.'''
class FileHandler:
    def __init__(self):
        self.__default_keys = [1073741906, 1073741903, 1073741904, 32, 97, 115]
        self.__wordList = ["Advance", "Turn Right", "Turn Left", "Shoot Fireball", "Shoot Flamethrower",
                           "Shoot Rocket"]

    def get_words_list(self):
        return self.__wordList

    '''this function writes to keys.txt the saved keys for each action. thus the playing keys are updates'''
    def writeToFile(self, wordsList, currentKeys):
        with open("keys.txt", "w") as file:
            file.write("**** DO NOT CHANGE THIS FILE!!!!!!****\n")
            file.write("keys:\n")

            for i in range(len(wordsList)):
                line = f"{wordsList[i]} = {currentKeys[i]}\n"
                file.write(line)

    '''this function reads from the file the current keys, used on initialization, for now it remains public as
    it should be used on game initialization to get the playing keys. it might move to "main" class
    (or future name - logicSupport)'''

    def readFromFile(self):
        settings = []

        try:
            with open("keys.txt", 'r') as file:
                lines = file.readlines()

                # Skip the first line (header)
                for line in lines[2:]:
                    line = line.strip()  # Remove leading/trailing whitespaces
                    if line:
                        key, value = line.split(' = ')
                        settings.append(int(value))
        except FileNotFoundError:
            self.writeToFile(self.__wordList, self.__default_keys)
            return self.__default_keys


        return settings