"""
mock_demo.py - Test case that uses mock objects, from Chapter 3 examples
"""

import sqlite3

from pytest import raises
from unittest.mock import Mock
from business_object.business_object import (
    BusinessObject, UserDao, Person, BusinessError
)


class TestBusinessObject:

    def test_get_user(self):
        expected_result = Person('Isaac', None, 'Newton')

        # create a mock for the DAO itself
        mock_dao = Mock(spec=UserDao)
        # create a mock for the DAO's query_user method and
        # set the return value of the mock method
        mock_dao.query_user.return_value = expected_result

        bus_obj = BusinessObject('mock_demo')
        # replace the real DAO with the mock DAO
        bus_obj.user_dao = mock_dao

        # when the business method is called, it will use the mock DAO
        # instead of the real DAO
        actual_result = bus_obj.get_user(123)

        # verify that the actual result equals the expected result
        assert actual_result == expected_result

    def test_get_user_not_found(self):
        mock_dao = Mock(spec=UserDao)
        mock_dao.query_user = Mock()
        mock_dao.query_user.return_value = None

        bus_obj = BusinessObject('mock_demo')
        bus_obj.user_dao = mock_dao

        with raises(ValueError):
            bus_obj.get_user(123)

    def test_get_user_dao_error(self):
        mock_dao = Mock(spec=UserDao)
        # Configure the mock query_user method to raise a DB error
        mock_dao.query_user.side_effect=sqlite3.Error('SQL error')

        bus_obj = BusinessObject('mock_demo')
        bus_obj.user_dao = mock_dao

        user_id = 123
        with self.assertRaisesRegex(BusinessError, 'SQL error'):
            bus_obj.get_user(user_id)
