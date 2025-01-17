"""Setup common test helpers."""

from unittest.mock import Mock

import aiohttp
from aioresponses import aioresponses
import pytest

from aioomada.controller import Controller


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture
async def omada_controller() -> Controller:
    """Returns the Omada controller.

    Clean up sessions automatically at the end of each test.
    """
    session = aiohttp.ClientSession()
    controller = Controller(
        "host", session, username="user", password="pass", callback=Mock()
    )
    yield controller
    await session.close()
