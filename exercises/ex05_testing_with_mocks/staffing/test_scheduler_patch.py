"""
mock_demo.py - Test case that uses the @patch decorator from unittet.mock,
from Chapter 3 examples
"""

from pytest import mark
from unittest.mock import patch, Mock
from staffing.provider import Provider
from staffing.scheduler import Scheduler, ProviderDao


class TestSchedulerWithPatching:
    # TODO: first, run only this first test case.
    # This test case doesn't use patching, so the production ProviderDao
    # constructor is called. This is bad for unit testing.
    def test_get_provider(self):
        expected_result = Provider(16430104, 'Isaac', None, 'Newton')
        mock_dao = Mock(spec=ProviderDao)
        mock_dao.query_provider.return_value = expected_result

        bus_obj = Scheduler('mock_demo')
        bus_obj.provider_dao = mock_dao

        actual_result = bus_obj.get_provider(16430104)

        assert actual_result == expected_result

    # The next text case patches the entire ProviderDao class; in other words,
    # when Scheduler calls the ProviderDao constructor, it will get a mock object
    # instead. The mock class is passed as the second argument of the test case.
    # TODO: after you run the first test case, delete @mark.skip here and
    #       run the tests again.
    @mark.skip
    @patch('staffing.scheduler.ProviderDao')
    def test_get_provider_skip_dao_constructor(self, mock_user_dao_class):
        mock_dao = mock_user_dao_class()
        expected_result = Provider(16430104, 'Isaac', None, 'Newton')
        mock_dao.query_provider.return_value = expected_result

        # Scheduler constructor's call to ProviderDao() now creates a mock
        scheduler = Scheduler('mock_demo')
        # no need to set Scheduler's user_dao

        actual_result = scheduler.get_provider(16430104)

        assert actual_result == expected_result

    # Patch the ProviderDao.query_provider method only. The mock for the patched
    # method will be passed as the test method's second argument.
    # @patch.object replaces only one method in the given class; the other
    # methods execute as usual
    # TODO: after you run the first test case, delete @mark.skip here and
    #       run the tests again.
    @mark.skip
    @patch.object(ProviderDao, 'query_provider')
    def test_get_provider_mock_one_method(self, mock_query_provider_method):
        expected_result = Provider(16430104, 'Isaac', None, 'Newton')
        # set the return value for the mock method
        mock_query_provider_method.return_value = expected_result

        scheduler = Scheduler('mock_demo')

        actual_result = scheduler.get_provider(16430104)

        assert actual_result == expected_result
