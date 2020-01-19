"""
mock_demo.py - Test case that uses the @patch decorator from unittet.mock,
from Chapter 3 examples
"""

from unittest import TestCase, main
from unittest.mock import patch
from person import Person
from business_object import BusinessObject, UserDao


class TestBusinessObject(TestCase):

    # Patch the UserDao.query_user method. The mock for the patched method
    # will be passed as the test method's second argument
    @patch.object(UserDao, 'query_user')
    def test_get_user(self, mock_query_user_method):
        expected_result = Person('Isaac', None, 'Newton')
        # set the return value for the mock method
        mock_query_user_method.return_value = expected_result

        bus_obj = BusinessObject('mock_demo')

        user_id = 123
        actual_result = bus_obj.get_user(user_id)

        mock_query_user_method.assert_called_with(user_id)
        self.assertEqual(expected_result, actual_result)

    @patch('business_object.UserDao')
    def test_get_user_skip_dao_constructor(self, mock_user_dao_class):
        mock_dao = mock_user_dao_class.return_value
        expected_result = Person('Isaac', None, 'Newton')
        mock_dao.query_user.return_value = expected_result

        # BusinessObject constructor's call to UserDao() now creates a mock
        bus_obj = BusinessObject('mock_demo')
        # no need to set BusinessObject's user_dao

        user_id = 123
        actual_result = bus_obj.get_user(user_id)

        mock_dao.query_user.assert_called_with(user_id)
        self.assertEqual(expected_result, actual_result)

if __name__ == '__main__':
    main()
