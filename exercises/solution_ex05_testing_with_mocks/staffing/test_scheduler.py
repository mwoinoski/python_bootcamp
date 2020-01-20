"""
Test cases that use mock objects
"""

from mysql.connector import DatabaseError

from pytest import raises
from unittest.mock import Mock
from staffing.scheduler import (
    Scheduler, ProviderDao, Provider, SchedulerError
)


class TestScheduler:

    def test_get_provider(self):
        expected_result = Provider(16430104, 'Isaac', None, 'Newton')

        # TODO: create a mock object. Set the `spec` argument value to ProviderDao
        mock_dao = Mock(spec=ProviderDao)

        # TODO: tell the mock ProviderDao to return expected_result
        #       when its query_provider method is called
        mock_dao.query_provider.return_value = expected_result

        # TODO: create a Scheduler object
        scheduler = Scheduler('mock_demo')

        # TODO; assign the mock DAO to the Scheduler's provider_dao attribute
        scheduler.provider_dao = mock_dao

        # TODO: call the Scheduler's get_provider method and save the result
        #       in a variable named actual_result
        actual_result = scheduler.get_provider(16430104)

        # TODO: verify actual_result equals expected_result
        assert actual_result == expected_result

    # TODO: after the previous test cases passes,
    #       uncomment the following test case, and then complete the code

    def test_get_provider_not_found(self):
        # TODO: note this test case will verify that if the DAO's query_provider
        #       method returns None, the Scheduler will raise a ValueError exception

        # TODO: create a mock object. Set the `spec` argument value to ProviderDao
        mock_dao = Mock(spec=ProviderDao)

        # TODO: tell the mock ProviderDao to return None
        #       when its query_provider method is called
        mock_dao.query_provider.return_value = None

        # TODO: create a Scheduler object
        scheduler = Scheduler('mock_demo')

        # TODO; assign the mock DAO to the Scheduler's provider_dao attribute
        scheduler.provider_dao = mock_dao

        # TODO: use the pytest `raises` function to detect a ValueError
        with raises(ValueError):
            # TODO: call the Scheduler's get_provider method
            # HINT: you don't need to store the method's return value because
            #       it will never be used
            scheduler.get_provider(16430104)

    # TODO: after the previous test cases passes,
    #       uncomment the following test case, and then complete the code

    def test_get_provider_dao_error(self):
        # TODO: note this test case will verify that if the DAO's query_provider
        #       method raises an exception, the Scheduler will raise a
        #       SchedulerError exception

        # TODO: create a mock object. Set the `spec` argument value to ProviderDao
        mock_dao = Mock(spec=ProviderDao)

        # TODO: tell the mock ProviderDao that when its query_provider method is
        #       called, it should have the side effect of raising a DatabaseError
        mock_dao.query_provider.side_effect = DatabaseError('SQL error')

        # TODO: create a Scheduler object
        scheduler = Scheduler('mock_demo')

        # TODO; assign the mock DAO to the Scheduler's provider_dao attribute
        scheduler.provider_dao = mock_dao

        # TODO: use the pytest `raises` function to detect a SchedulerError
        with raises(SchedulerError):
            # TODO: call the Scheduler's get_provider method
            scheduler.get_provider(16430104)
