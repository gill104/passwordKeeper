#! python3

import pickle
import os.path
import random
import string
import sys
import pyperclip


class Passwords:
    def __init__(self):
        print('here')
        self._key = ''
        self._password = ''
        self._noSpace = True
        self._minLength = False
        self._capLetter = False
        self._weirdSymbol = False
        self._hasLetter = False
        self._hasNumber = False
        self._passList = {}
        self._mypath = '/home/gill/Desktop/passwordKeeper/newFile.pickle'

        if os.path.isfile(self._mypath):
            with open("newFile.pickle", "rb") as handle:
                self._passList = pickle.load(handle)
        else:
            with open("newFile.pickle", "wb") as handle:
                pickle.dump(self._passList,handle,protocol=pickle.HIGHEST_PROTOCOL)
            with open("newFile.pickle", 'rb') as handle:
                self.passList = pickle.load(handle)

    def _getPasswordLength(self):
        return len(self._password)

    def _setPassword(self, p):
        self._password = p

    def _setKey(self, k):
        self._key = k

    def _generatePassword(self):
        randPas = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(12)])
        self._setPassword(randPas)

    def _addKeyValue(self):
        self._passList.update({str(self._key):str(self._password)})
        with open('newFile.pickle','wb') as handle:
            pickle.dump(self._passList,handle,protocol=pickle.HIGHEST_PROTOCOL)
        input('Press enter to continue...')

    def _searchForKey(self):
        if self._key in self._passList:
            return True
        return False

    def _searchForExistingKey(self, k):
        print('searching')
        if k in self._passList:
            self._setKey(k)
            self._setPassword(self._passList[self._key])
            return True
        return False

    def _checkIfValidLength(self):
        pLen = self._getPasswordLength()
        if pLen > 7:
            self._minLength = True
        else:
            input('Password not a long enough!!')
            
    def _checkifValidInput(self):

        """ print('\n\nmyPass: ', myPass)
        print('myPass Length: ', self._getPasswordLength())
        print('position: ', position) """
        position = 0
        while position < self._getPasswordLength():
            if str(self._password[position]).isspace():
                self._noSpace = False
                break
            if str(self._password[position]).isdigit():
                self._hasNumber = True
                position += 1

            elif str(self._password[position]).isalpha():
                self._hasLetter = True
                print('alpha pLen[i]:', self._password[position])
                if str(self._password[position]).isupper():
                    self._capLetter = True
                position += 1
            else:
                print('None pLen[i]:', self._password[position])
                position += 1
                self._weirdSymbol = True

        if not self._weirdSymbol:
            input('No weird Symbol in password!!')

    def _addInformation(self, key, pas):
        self._setKey(key)
        if pas == '!gen':
            self._generatePassword()
        else:
            self._setPassword(pas)

        if not bool(self._passList):
            self._checkValidation()
            print('was empty adding items')
        else:
            self._addKeyPair()

    def _checkValidation(self):
        self._checkIfValidLength()
        self._checkifValidInput()
        if self._minLength and self._weirdSymbol and self._capLetter:
            input('updated new key-value')
            self._addKeyValue()

    def _addKeyPair(self):
        foundKey = self._searchForKey()
        if not foundKey:
            print('No key found')
            self._checkValidation()
        else:
            changeKey = input('Do you want to update existing key?')
            if changeKey == 'y':
                self._checkValidation()
            else:
                input('req not met!')

    def _getPassFromDict(self, k):
        if self._searchForExistingKey(k):
            print('Key Exists')
            print('key: ', self._key)
            print('value: ', self._password)
            input('Current Items. \nPress enter to continue...')
        else:
            print('No account in database')

    def printDictionary(self):
        for k, v in self._passList.items():
            print('key: ' + k)
            print('value: ' + v)
        input('Current Items. \nPress enter to continue...')

    def showLocation(self):
        return self._key

    def showPassword(self):
        return self._password


def switchInput(inputValue):
    switchDict = {
        '!display': 0,
        '!q': 1,
        'input': 2,
        'find': 3,
    }
    return switchDict.get(inputValue, "none")


def main():
    p = Passwords()
    if len(sys.argv) < 2:
        print('Usage: python pw.py[account] - copy account password')
        app_on = True
        while app_on:
            os.system('cls' if os.name == 'nt' else 'clear')
            takeMeTo = input('\'!display\', \'input\', \'!q\'\nWhat do you want to do? ')
            iv = switchInput(takeMeTo)
            if iv == 0:
                p.printDictionary()
            elif iv == 1:
                app_on = False
            elif iv == 2:
                key = input('Enter Key:')
                value = input('Enter Value:')
                p._addInformation(key, value)
            elif iv == 3:
                key = input('Enter Key:')

            else:
                print('invalid input')
        sys.exit()
    else:
        account = sys.argv[1] #first command line arg is the account name
        print('Account: {}'.format(account))
        p._getPassFromDict(account)

if __name__ == "__main__":
    main()