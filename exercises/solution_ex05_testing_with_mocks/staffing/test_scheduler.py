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

        mock_dao = Mock(spec=ProviderDao)

        mock_dao.query_provider.return_value = expected_result

        scheduler = Scheduler('mock_demo')

        scheduler.provider_dao = mock_dao

        actual_result = scheduler.get_provider(16430104)

        assert actual_result == expected_result

    def test_get_provider_not_found(self):
        mock_dao = Mock(spec=ProviderDao)

        mock_dao.query_provider.return_value = None

        scheduler = Scheduler('mock_demo')

        scheduler.provider_dao = mock_dao

        with raises(ValueError):
            scheduler.get_provider(16430104)

    def test_get_provider_dao_error(self):
        mock_dao = Mock(spec=ProviderDao)

        mock_dao.query_provider.side_effect = \
            DatabaseError('SQL error')

        scheduler = Scheduler('mock_demo')

        scheduler.provider_dao = mock_dao

        with raises(SchedulerError):
            scheduler.get_provider(16430104)
