#!/usr/bin/env python
from sqlite3 import DatabaseError

from db_utils import Table, SQLiteDatabase


class User(Table):
    """User table of user database."""
    table_name = 'User'
    primary_key = 'Username'

    def update_password(self, username, password):
        """Updates the 'Password' field of a given user.

        :param username: primary key of user to change password
        :param password: new password to change to
        :type username: str
        :type password: str
        """
        self.update(('Password', password), username)

    def update_picture(self, username, picture):
        """Updates the 'Picture' field of a given user.

        :param username: primary key of user to change picture
        :param picture: new picture to upload
        :type username: str
        :type picture: bytes
        """
        self.update(('Picture', picture), username)


class UserDatabase(SQLiteDatabase):
    """Controller for SQL user database."""

    def add_user(self, username, password, permissions):
        user_info = {'Username': username, 'Password': password,
                     'Permissions': permissions}
        User(self).add(user_info)

    def check_permissions(self, username):
        user = User(self).get(username)
        return user['Permissions']

    def authorize(self, username):
        """Check the authorization of a given user.

        :param username: primary key of User table
        :type username: str
        :return: whether a given user has authorization
        :rtype: bool
        """
        user = User(self).get(username)
        if not user:
            raise DatabaseError("User does not exist.")
        return user['Permissions'] == 'MANAGER'

    def validate_login(self, username, password):
        """Validate a user login.

        :param username: primary key of User table
        :param password: password to verify
        :type username: str
        :type password: str
        :return: whether user login info is correct
        :rtype: bool
        """
        user = User(self).get(username)
        return user and user['Password'] == password

    def update_password(self, username, password):
        User(self).update_password(username, password)

    def update_picture(self, username, picture):
        User(self).update_picture(username, picture)
