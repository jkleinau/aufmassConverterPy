# CreateCred.py
# Creates a credential file.
from cryptography.fernet import Fernet
import re
import ctypes
import time
import os
import sys


class Credentials:

    def __init__(self, username="matthias.herzog", api_key="dd0c7925689fbf4f2083412497c30f9d2445",
                 customer_ID="5c7ef0e0b4132", expiry_time=-1):

        self.__username = username
        self.__api_key = api_key
        self.__key = Fernet.generate_key()
        self.__customer_ID = customer_ID
        self.__key_file = 'resources/cred/key.key'
        self.__time_of_exp = expiry_time

    # ----------------------------------------
    # Getter setter for attributes
    # ----------------------------------------
    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key):
        f = Fernet(self.__key)
        self.__api_key = f.encrypt(api_key.encode()).decode()
        del f

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        while username == '':
            username = input('Enter a proper User name, blank is not accepted:')
        self.__username = username

    @property
    def customer_ID(self):
        return self.__customer_ID

    @customer_ID.setter
    def customer_ID(self, custome_ID):
        f = Fernet(self.__key)
        self.__customer_ID = f.encrypt(custome_ID.encode()).decode()
        del f

    @property
    def expiry_time(self):
        return self.__time_of_exp

    @expiry_time.setter
    def expiry_time(self, exp_time):
        if exp_time >= 2:
            self.__time_of_exp = exp_time

    def create_cred(self):
        """
        This function is responsible for encrypting the password and create  key file for
        storing the key and create a credential file with user name and password
        """

        cred_filename = 'resources/cred/CredFile.ini'

        with open(cred_filename, 'w') as file_in:
            file_in.write("#Credential file:\nUsername={}\nAPI_Key={}\nCustomer_ID={}\nExpiry={}\n"
                          .format(self.__username, self.__api_key, self.__customer_ID, self.__time_of_exp))
            file_in.write("++" * 20)

            # If there exists an older key file, This will remove it.
        if os.path.exists(self.__key_file):
            os.remove(self.__key_file)

            # Open the Key.key file and place the key in it.
        # The key file is hidden.
        try:
            os_type = sys.platform
            if os_type == 'linux':
                self.__key_file = '.' + self.__key_file

            with open(self.__key_file, 'w') as key_in:
                key_in.write(self.__key.decode())
                # Hidding the key file. The below code snippet finds out which current os the scrip is running on and
                # does the taks base on it.
                if os_type == 'win32':
                    ctypes.windll.kernel32.SetFileAttributesW(self.__key_file, 2)
                else:
                    pass

        except PermissionError:
            os.remove(self.__key_file)
            print("A Permission error occurred.\n Please re run the script")
            sys.exit()

        self.__username = ""
        self.__customer_ID = ""
        self.__key = ""
        self.__key_file

    def get_cred(self):
        key = ''

        with open('resources/cred/key.key', 'r') as key_in:
            key = key_in.read().encode()

        f = Fernet(key)
        with open('resources/cred/CredFile.ini', 'r') as cred_in:
            lines = cred_in.readlines()
            config = {}
            for line in lines:
                tuples = line.rstrip('\n').split('=', 1)
                if tuples[0] in ('Username', 'Customer_ID', 'API_Key'):
                    config[tuples[0]] = tuples[1]

            customer_ID = f.decrypt(config['Customer_ID'].encode()).decode()
            api_key = f.decrypt(config['API_Key'].encode()).decode()
            return customer_ID, api_key


def main():
    # Creating an object for Credentials class
    creds = Credentials()

    # Accepting credentials
    creds.username = "matthias.herzog"
    creds.api_key = "dd0c7925689fbf4f2083412497c30f9d2445"
    creds.customer_ID = "5c7ef0e0b4132"
    creds.expiry_time = -1

    # calling the Credit
    creds.create_cred()
    print("**" * 20)
    print("Cred file created successfully at {}"
          .format(time.ctime()))

    if not (creds.expiry_time == -1):
        os.startfile('expire.py')

    print("**" * 20)

    print(creds.get_cred())


if __name__ == "__main__":
    main()
