from __future__ import annotations

import pytest

import aiordr

from .classes import MockResponse


@pytest.fixture
def client() -> aiordr.ordrClient:
    return aiordr.ordrClient(developer_mode="devmode_success")


@pytest.fixture
def client_fail() -> aiordr.ordrClient:
    return aiordr.ordrClient(developer_mode="devmode_fail")


@pytest.fixture
def client_wsfail() -> aiordr.ordrClient:
    return aiordr.ordrClient(developer_mode="devmode_wsfail")


@pytest.fixture
def skins() -> bytes:
    with open("tests/data/multiple_skin.json", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def render_servers() -> bytes:
    with open("tests/data/multiple_render_server.json", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def render_add() -> bytes:
    with open("tests/data/render_add.json", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def skin_custom() -> bytes:
    with open("tests/data/single_skin_custom.json", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def server_onlinecount() -> bytes:
    with open("tests/data/server_onlinecount.txt", "rb") as f:
        data = f.read()
    return data


class TestClient:
    @pytest.mark.asyncio
    async def test_get_skins(
        self,
        mocker,
        client: aiordr.ordrClient,
        skins: bytes,
    ) -> None:
        resp = MockResponse(skins, 200)
        async with client:
            mocker.patch.object(client._session, "get", return_value=resp)
            data = await client.get_skins()
            assert isinstance(data, aiordr.models.SkinsResponse)

    @pytest.mark.asyncio
    async def test_get_server_list(
        self,
        mocker,
        client: aiordr.ordrClient,
        render_servers: bytes,
    ) -> None:
        resp = MockResponse(render_servers, 200)
        async with client:
            mocker.patch("aiohttp.ClientSession.get", return_value=resp)
            data = await client.get_server_list()
            assert isinstance(data, list) and all(
                isinstance(x, aiordr.models.RenderServer) for x in data
            )

    @pytest.mark.asyncio
    async def test_get_server_online_count(
        self,
        mocker,
        client: aiordr.ordrClient,
        server_onlinecount: bytes,
    ) -> None:
        resp = MockResponse(server_onlinecount, 200)
        async with client:
            mocker.patch("aiohttp.ClientSession.get", return_value=resp)
            data = await client.get_server_online_count()
            assert isinstance(data, int)

    @pytest.mark.asyncio
    async def test_get_custom_skin(
        self,
        mocker,
        client: aiordr.ordrClient,
        skin_custom: bytes,
    ) -> None:
        resp = MockResponse(skin_custom, 200)
        async with client:
            mocker.patch("aiohttp.ClientSession.get", return_value=resp)
            data = await client.get_custom_skin(1)
            assert isinstance(data, aiordr.models.SkinCompact)
