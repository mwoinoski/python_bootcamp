"""
scheduler.py - Classes for exercising mock objects
"""

from mysql.connector import DatabaseError
from staffing.provider import Provider


class ProviderDao:
    def __init__(self) -> None:
        print('\ncreating a production ProviderDao')

    def query_provider(self, provider_id: int) -> Provider:
        print('\ncalled query_provider method production ProviderDao')
        return Provider(123, 'Isaac', None, 'Newton')


class Scheduler:
    provider_dao: ProviderDao
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
        self.provider_dao = ProviderDao()

    def get_provider(self, provider_id: int) -> Provider:
        """ Business method for Scheduler class """
        if provider_id is None or provider_id < 1:
            raise ValueError(f'invalid provider ID "{provider_id}"')
        try:
            provider: Provider = \
                self.provider_dao.query_provider(provider_id)
            if provider is None:
                raise ValueError(f'{provider_id} is not a valid provider ID')

            return provider
        except DatabaseError as ex:
            raise SchedulerError(
                f'Problem fetching provider with ID {provider_id}: {ex}')

    def __str__(self) -> str:
        return f"{self.name}"


class SchedulerError(Exception):
    """ Application-specific exception class """
    pass
