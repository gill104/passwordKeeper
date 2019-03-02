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
    return location


class Passwords:
    def __init__(self):
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
        saves the dictionary _passlist to a .pickle file
    """
    def _savePickleFile(self):
        with open('newFile.pickle', 'wb') as handle:
            pickle.dump(self._passList, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self._resetParameters()
        input('Saved information\nPress enter to continue...')

    """
        Checks if given location exists within dictionary if so then it searches for username within that location
        returns a T/F 
    """
    def _searchForLoc(self):
        if self._loc in self._passList:
            for username, password in self._passList[self._loc].items():
                if username == self._user:
                    return True
            return False

    """
        Sets the location and username that were inputed by the user; normalize the location to remove spaces and upper-
        case letters. Loops if the password is set incorrectly by the user until they enter a correct password
    """
    # add a filter to location spaces == _ and all lowercase
    def _addInformation(self, loc, user, pas):
        self._setUser(user)
        self._setLoc(_normalizeLocation(loc))

        looping = self._passwordLoop(pas)

        while not looping:
            os.system('cls' if os.name == 'nt' else 'clear')
            self._resetPasswordParameters()
            pas = input('Re-enter a new password: ')
            looping = self._passwordLoop(pas)
        self._checkUserName()

    """
        Gets the password information checks whether to generate a password for use user inputed password. Here password
        is send to get validated returning a T/F back to _addInformation
    """
    def _passwordLoop(self, pas):
        if '!gen' in pas:
            val = pas.split(' ')
            # for user defined length
            if len(val) > 1:
                self._generatePassword(val[1])
                return True
            elif len(val) <= 1:
                self._generatePassword(val[0])
                return True
            else:
                return False

        self._setPassword(pas)
        self._checkPasswordValidation()
        self._passwordFlags()
        # if the list is empty calls check validation for password

        if self._accepted:
            if not bool(self._passList):
                return True
            else:
                return True
        else:
            print('Bad Password')
            return False

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
        self._checkPasswordValidation()

        if not self._passwordFlags():
            self._resetPasswordParameters()
            self._generatePassword(v)

    """
        Checks the boolean conditions for the password to trigger _accepted. If _accepted it returns true since no need
        to recheck an accepted password
    """
    def _passwordFlags(self):
        if self._accepted:
            return True
        else:

            if self._minLength and self._weirdSymbol and self._capLetter and self._hasNumber and self._hasLetter and self._noSpace:
                print('Password Accepted:', self._password)
                self._accepted = True
                return True
            else:
                print('Invalid password given')
                return False

    """
        Checks the length and conditionals on the password
    """
    def _checkPasswordValidation(self):
        self._checkIfValidLength()
        self._checkifValidInput()

    """
        adds the information given by the user to _passlist and calls to save to .pickle file
    """
    def _sendIt(self):

        if self._accepted:
            # creates a new dictionary to place within self._passList else just adds to existing items
            if self._loc not in self._passList:
                self._passList[self._loc] = {}
                self._passList[self._loc][self._user] = self._password
            else:
                self._passList[self._loc][self._user] = self._password
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
            print(pLen)
            print('Error: Invalid length')

    """
        Validates user inputed password; ticks off flags to make sure password is correct
    """
    def _checkifValidInput(self):
        position = 0
        while position < len(self._password):
            if str(self._password[position]).isspace():
                self._noSpace = False
                print('Error: Space in password')
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
        if not self._capLetter:
            print('Error: No capital letter')
        if not self._hasLetter:
            print('Error: No letters')
        if not self._hasNumber:
            print('Error: No Numbers')

    """
        Checks if there is an existing key that the user inputed if yes, asks if user wants to replace password else do
        nothing.
    """
    def _checkUserName(self):
        dupeUserName = self._searchForLoc()
        # input(dupeUserName)
        if dupeUserName:
            changeLoc = input('Username\Password exists...Want to update password?')
            if changeLoc == 'y':
                self._sendIt()
            else:
                input('Returning to menu!')
        else:
            self._sendIt()

    """
        Gets the password associated with username from location inputted by user. Also saves to clipboard
    """
    def _getPassFromDict(self, l, u):
        if self._searchForExistingLoc(l, u):
            print('Password: ', self._password)
            """
                If using linux: “sudo apt-get install xclip” 
            """
            pyperclip.copy(str(self._password))
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
        the information to the user. Used for command line input
    """
    def _searchForExistingLoc(self, l, u):
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
        input('Press enter to continue...')

    def _resetPasswordParameters(self):
        self._noSpace = True
        self._minLength = False
        self._capLetter = False
        self._weirdSymbol = False
        self._hasLetter = False
        self._hasNumber = False
        self._accepted = False

    def _resetParameters(self):
        self._resetPasswordParameters()
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
