"""
Created on 22 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/2520893/how-to-flush-the-input-stream-in-python

example document:
{"email": "bruno.beloff@southcoastscience.com", "password": "hello"}
"""

import json
import sys
import termios

from collections import OrderedDict
from getpass import getpass

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserCredentials(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "cognito_user_credentials.json"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def from_stdin(cls):
        line = sys.stdin.readline()
        jdict = json.loads(line)

        return cls.construct_from_jdict(jdict)


    @classmethod
    def from_user(cls):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)               # flush stdin
        except termios.error:
            pass

        print("Enter email address: ", end="", file=sys.stderr)
        email = input().strip()

        print("Enter password: ", end="", file=sys.stderr)
        password = input().strip()

        return cls(email, password)


    @staticmethod
    def password_from_user():
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)               # flush stdin
        except termios.error:
            pass

        return getpass().strip()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None) if skeleton else None

        email = jdict.get('email')
        password = jdict.get('password')

        return cls(email, password)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email, password):
        """
        Constructor
        """
        super().__init__()

        self.__email = email                            # string
        self.__password = password                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def ok(self):
        if not self.email or not self.password:
            return False

        if not Datum.is_email_address(self.email):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email'] = self.email
        jdict['password'] = self.password

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email(self):
        return self.__email


    @property
    def password(self):
        return self.__password


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserCredentials:{email:%s, password:%s}" %  (self.email, self.password)


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserIdentity(object):
    """
    classdocs
    """
    USER = "username"
    EMAIL = "email"
    GIVEN_NAME = "given_name"
    FAMILY_NAME = "family_name"
    PASSWORD = "password"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_body(cls, body):
        if not body:
            return None

        jdict = json.loads(body)

        email = jdict[cls.EMAIL]
        given_name = jdict[cls.GIVEN_NAME]
        family_name = jdict[cls.FAMILY_NAME]
        password = jdict[cls.PASSWORD]

        return cls(None, email, given_name, family_name, password)


    @classmethod
    def construct_from_response(cls, res, multiples=False):
        if not res:
            return None

        username = res['Username']

        final_d = {}
        attrs = res['Attributes'] if multiples else res['UserAttributes']

        for attr in attrs:
            nk = None
            for value in attr.values():
                if nk:
                    final_d[nk] = value
                    break

                nk = value
        try:
            return cls(username, final_d['email'], final_d['given_name'], final_d['family_name'], None)
        except KeyError:
            return None


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None, None, None, None) if skeleton else None

        username = jdict.get('username')
        email = jdict.get('email')
        given_name = jdict.get('given-name')
        family_name = jdict.get('family-name')
        password = jdict.get('password')
        is_super = jdict.get('is-super')

        return cls(username, email, given_name, family_name, password, is_super=is_super)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, username, email, given_name, family_name, password, is_super=False):
        """
        Constructor
        """
        self.__username = username                          # string (int)
        self.__email = email                                # string
        self.__given_name = given_name                      # string
        self.__family_name = family_name                    # string
        self.__password = password                          # string
        self.__is_super = bool(is_super)                    # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email'] = self.email
        jdict['password'] = self.password
        jdict['given-name'] = self.given_name
        jdict['family-name'] = self.family_name
        jdict['is-super'] = self.is_super

        return jdict

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__username


    @property
    def email(self):
        return self.__email


    @property
    def given_name(self):
        return self.__given_name


    @property
    def family_name(self):
        return self.__family_name


    @property
    def password(self):
        return self.__password


    @property
    def is_super(self):
        return self.__is_super


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoUserIdentity:{username:%s, email:%s, given_name:%s, family_name:%s, is_super:%s}" % \
               (self.username, self.email, self.given_name, self.family_name, self.is_super)
