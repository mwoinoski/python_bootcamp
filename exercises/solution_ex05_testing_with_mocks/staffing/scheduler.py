"""
scheduler.py - Classes for exercising mock objects
"""

from mysql.connector import DatabaseError

from staffing.provider import Provider


# TODO: note the ProviderDao class. Our unit tests need to replace ProviderDao
#       with mock objects.
class ProviderDao:
    def __init__(self) -> None:
        print('creating a production ProviderDao')
        # Production DAO would create connection to database, etc.

    def query_provider(self, provider_id: int) -> Provider:
        print('called query_provider method production ProviderDao')
        return Provider(123, 'Isaac', None, 'Newton')
        # Production DAO would query database for provider by ID


class Scheduler:
    # TODO: note the Scheduler has a dependency on the ProviderDao class.
    provider_dao: ProviderDao
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
        # TODO: note the Scheduler has a dependency on the ProviderDao class.
        self.provider_dao = ProviderDao()

    def get_provider(self, provider_id: int) -> Provider:
        """ Business method for Scheduler class """
        if provider_id is None or provider_id < 1:
            raise ValueError(f'invalid provider ID "{provider_id}"')
        try:
            # TODO: note the call to the DAO's query_provider method
            provider: Provider = self.provider_dao.query_provider(provider_id)
            if provider is None:
                raise ValueError(f'{provider_id} is not a valid provider ID')

            return provider
        # TODO: note that if the DAO raises a DatabaseError, the Scheduler
        #       should raise a SchedulerError
        except DatabaseError as ex:
            raise SchedulerError(
                f'Problem fetching provider with ID {provider_id}: {ex}')

    def __str__(self) -> str:
        return f"{self.name}"


class SchedulerError(Exception):
    """ Application-specific exception class """
    pass
