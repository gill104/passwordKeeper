#! python3

import pickle
import os.path
import random
import string
import sys
import pyperclip


def _normalizeLocation(loc):
    location = ''
    for x in loc:
        if x == ' ':
            location += '_'
        else:
            location += x.lower()
    # print(location)
    return location


class Passwords:
    def __init__(self):
        print('here')
        self._loc = ''
        self.user = ''
        self._password = ''
        self._noSpace = True
        self._minLength = False
        self._capLetter = False
        self._weirdSymbol = False
        self._hasLetter = False
        self._hasNumber = False
        self._accepted = False
        self._passList = {}
        self._mypath = '/home/gill/Desktop/passwordKeeper/newFile.pickle'

        """
            _passList = {location : password}
                | 
                V
            _passList = {location : {user: password}, {user2: password}
        """
        if os.path.isfile(self._mypath):
            with open("newFile.pickle", "rb") as handle:
                self._passList = pickle.load(handle)
        else:
            with open("newFile.pickle", "wb") as handle:
                pickle.dump(self._passList, handle, protocol=pickle.HIGHEST_PROTOCOL)
            with open("newFile.pickle", 'rb') as handle:
                self.passList = pickle.load(handle)

    def _setPassword(self, p):
        self._password = p

    def _setLoc(self, k):
        self._loc = k

    def _setUser(self, u):
        self._user = u

    """
        Adds the loc-pair value to the dictionary [_passList] and updates the .pickle file with the new dictionary info
    """
    def _savePickleFile(self):
        with open('newFile.pickle', 'wb') as handle:
            pickle.dump(self._passList, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self._resetParameters()
        input('Press enter to continue...')

    """
        Searches the dictionary to check if the key of the class exists within it
    """
    def _searchForLoc(self):
        if self._loc in self._passList:
            for username, password in self._passList[self._loc].items():
                if username == self._user:
                    return True
            return False
        """for location, user in self._passList.items():
            for u1, p, in user.items():
                if u1 == self._user and location == self._loc:
                    return True
        return False"""

    """
        Gets the key and password from user and checks if its a user inputed password or to generate a password
        calls the appropriate method
    """
    # add a filter to location spaces == _ and all lowercase
    def _addInformation(self, loc, user, pas):
        self._setUser(user)
        self._setLoc(_normalizeLocation(loc))

        if '!gen' in pas:
            val = pas.split(' ')
            # for user defined length
            if len(val) > 1:
                #print(val[1])
                self._generatePassword(val[1])
            else:
                self._generatePassword(val[0])
        else:
            self._setPassword(pas)

        # if the list is empty calls check validation for password

        if not bool(self._passList):
            self._checkPasswordValidation()
            print('was empty adding items')
        else:
            self._checkUserName()

    """
        Generates a password depending whether or not a valid length of was provided. If no valid length it goes to 
        default value of 12. Sets the random password to be a combination of letters(cap and lower digits and symbols
    """
    def _generatePassword(self, v):
        if v.isdigit():
            pasLength = int(v)
        else:
            pasLength = 6

        randPas = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation)
                           for n in range(pasLength)])

        self._setPassword(randPas)

        self._checkifValidInput()
        self._checkIfValidLength()
        if not self._passwordFlags():
            self._generatePassword(v)

    def _passwordFlags(self):
        if not self._accepted:
            if self._minLength and self._weirdSymbol and self._capLetter and self._hasNumber and self._hasLetter and self._noSpace:
                print('Password Accepted: ', self._password)
                self._accepted = True
                return True
            print('Invalid password given')
            return False
        else:
            pass

    """
        Checks password. Calls to see if length and valid inputs. If corrects adds 
    """
    def _checkPasswordValidation(self):
        self._checkIfValidLength()
        self._checkifValidInput()
        if self._accepted or self._passwordFlags():
            # creates a new dictionary to place within self._passList else just adds to existing items
            if self._loc not in self._passList:
                self._passList[self._loc] = {}
                self._passList[self._loc][self._user] = self._password
            else:
                self._passList[self._loc][self._user] = self._password
                input('updated new key-value')
            self._savePickleFile()
        else:
            print('Not all conditions met!')

    """
        Checks the length of the password for a valid length set to 5 or greater as default
    """
    def _checkIfValidLength(self):
        pLen = len(self._password)
        if pLen > 5:
            self._minLength = True
        else:
            print('Error: Invalid length')
            input('Press any button to cont...')

    """
        Validates user inputed password; ticks off flags to make sure password is correct
    """
    def _checkifValidInput(self):
        position = 0
        while position < len(self._password):
            if str(self._password[position]).isspace():
                self._noSpace = False
                print('Error: Space in password')
                input('Press any button to cont...')
                break
            if str(self._password[position]).isdigit():
                self._hasNumber = True
                # print('digit pLen[i]:', self._password[position])
                position += 1

            elif str(self._password[position]).isalpha():
                self._hasLetter = True
                # print('alpha pLen[i]:', self._password[position])
                if str(self._password[position]).isupper():
                    self._capLetter = True
                position += 1
            else:
                # print('None pLen[i]:', self._password[position])
                position += 1
                self._weirdSymbol = True

        if not self._weirdSymbol:
            print('Error: No weird Symbol')
            input('Press any button to cont...')

    """
        Checks if there is an existing key that the user inputed if yes, asks if user wants to replace password else do
        nothing. Also checks for password validation if all correct saves to .pickle file
    """
    def _checkUserName(self):
        dupeUserName = self._searchForLoc()
        # input(dupeUserName)
        if dupeUserName:
            changeLoc = input('Username\Password exists...Want to update password?')
            if changeLoc == 'y':
                self._checkPasswordValidation()
            else:
                input('Press any button cont...')
        else:
            self._checkPasswordValidation()

    """
        Gets the password from user inputed loc if loc exists
    """
    def _getPassFromDict(self, l, u):
        if self._searchForExistingLoc(l, u):
            # print('loc Exists')
            # print('loc: ', self._loc)
            print('Password: ', self._password)
            input('\nPress enter to continue...')
        else:
            print('No User in database')

    """
        Lists the users in the dictionary from the given location
    """
    def _getUsersFromDict(self, l):
        userList = ""
        for location, user in self._passList.items():
            for u1, p in user.items():
                if location == l:
                    userList += u1 + ' '
        return userList

    """
        Searches the loc given by the user. If found sets both the loc and password to the class in order to retrive 
        the information to the user
    """
    def _searchForExistingLoc(self, l, u):
        # print('searching')
        for location, user in self._passList.items():
            for u1, p1 in user.items():
                if location == l and u1 == u:
                    self._setLoc(l)
                    self._setPassword(self._passList[self._loc][u1])
                    return True
        return False

    """
        prints dictionary items
    """
    def printDictionary(self):
        # location and inner dictionary
        for l, u in self._passList.items():
            # user and password from inner dictionary
            for u1, p in u.items():
                print('loc: ',  l)
                print('value: ', u1)
                print('password:', p)
        input('Current Items. \nPress enter to continue...')

    def _resetParameters(self):
        self._noSpace = True
        self._minLength = False
        self._capLetter = False
        self._weirdSymbol = False
        self._hasLetter = False
        self._hasNumber = False
        self._loc = ''
        self._password = ''
        self._user = ''

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
            # rests all parameters of the password
            p._resetParameters()

            os.system('cls' if os.name == 'nt' else 'clear')
            takeMeTo = input('\'!display\', \'input\', \'!q\'\nWhat do you want to do? ')
            iv = switchInput(takeMeTo)
            if iv == 0:
                p.printDictionary()
            elif iv == 1:
                app_on = False
            elif iv == 2:
                loc = input('Enter Location: ')
                username = input('Enter Username: ')
                value = input('Enter Password: ')

                p._addInformation(loc, username, value)
            elif iv == 3:
                loc = input('Enter loc:')

            else:
                print('invalid input')
        sys.exit()
    else:
        if len(sys.argv) == 2:
            account = sys.argv[1]  # first command line arg is the account name
            print('Account: {}'.format(account))
            print(p._getUsersFromDict(account))
        else:
            account = sys.argv[1]  # first command line arg is the account name
            user = sys.argv[2]
            print('Account: {}'.format(account))
            print('User: {}'.format(user))
            p._getPassFromDict(account, user)


if __name__ == "__main__":
    main()
