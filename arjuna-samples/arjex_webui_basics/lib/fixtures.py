
import pytest

@pytest.fixture(scope="session")
def get_number(request):
    yield 2