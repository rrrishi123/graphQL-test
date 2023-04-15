import pytest
from gql_client import execute_gql_query


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an instance of the default event loop for each test session.
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def gql_client():
    """
    Fixture to provide a GraphQL client instance.
    """
    yield execute_gql_query
