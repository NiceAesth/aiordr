"""This module contains the client for interfacing with the o!rdr API."""
from __future__ import annotations

import functools
from typing import Literal
from typing import TYPE_CHECKING
from warnings import warn

import aiohttp
import orjson
from aiolimiter import AsyncLimiter
from socketio import AsyncClient as sio_async  # type: ignore

from .exceptions import APIException
from .helpers import add_param
from .helpers import from_list
from .models import ErrorCode
from .models import RenderAddEvent
from .models import RenderCreateResponse
from .models import RenderFailEvent
from .models import RenderFinishEvent
from .models import RenderOptions
from .models import RenderProgressEvent
from .models import RenderServer
from .models import RendersResponse
from .models import SkinCompact
from .models import SkinsResponse

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Any
    from typing import Type
    from typing import Union
    from typing import Optional
    from typing import Callable


__all__ = ("ordrClient",)

ClientRequestType = Literal["GET", "POST", "DELETE", "PUT", "PATCH"]


def get_content_type(content_type: str) -> str:
    """Returns the content type."""
    return content_type.split(";")[0]


DeveloperModes = Literal["devmode_success", "devmode_fail", "devmode_wsfail"]


class ordrClient:
    def __init__(self, **kwargs: Any) -> None:
        r"""o!rdr API client.
        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *developer_mode* (``DeveloperModes``) --
                Optional, defaults to None
            * *verification_key* (``str``) --
                Optional, defaults to None. If not provided, rate limits will be forced to 1 request per 5 minutes
            * *limiter* (``tuple[int, int]``) --
                Optional, rate limit, defaults to (1, 300) (1 requests per 5 minutes)
        """
        self._developer_mode: Optional[str] = kwargs.pop("developer_mode", None)
        self._verification_key: Optional[str] = kwargs.pop("verification_key", None)

        if self._developer_mode:
            if self._verification_key:
                warn(
                    "You are running in developer mode. This means that your requests will be simulated and your verification key will not be used.",
                )
            self._verification_key = self._developer_mode

        self._session: Optional[aiohttp.ClientSession] = None
        self._base_url: str = "https://apis.issou.best"
        self._websocket_url: str = "https://ordr-ws.issou.best"

        max_rate, time_period = kwargs.pop("limiter", (1, 300))
        if (max_rate / time_period) > (10 / 60):
            warn(
                "You are running at an insanely high rate limit. Doing so may result in your account being banned.",
            )

        if not self._verification_key:
            max_rate = 1
            time_period = 300

        self._limiter: AsyncLimiter = AsyncLimiter(
            max_rate=max_rate,
            time_period=time_period,
        )

        self.socket = sio_async()

    def on_render_added(self, func: Callable) -> Callable:
        r"""Returns a callable that is called when a render is added, to be used as:
        @client.on_render_added()
        async def render_added(event: RenderAddEvent):
        """

        @functools.wraps(func)
        async def wrapper(data: dict) -> Any:
            return await func(RenderAddEvent.parse_obj(data))

        self.socket.on("render_added_json", wrapper)
        return wrapper

    def on_render_progress(self, func: Callable) -> Callable:
        r"""Returns a callable that is called when a render is updated, to be used as:
        @client.on_render_progress()
        async def render_progress(event: RenderProgressEvent):
        """

        @functools.wraps(func)
        async def wrapper(data: dict) -> Any:
            return await func(RenderProgressEvent.parse_obj(data))

        self.socket.on("render_progress_json", wrapper)
        return wrapper

    def on_render_fail(self, func: Callable) -> Callable:
        r"""Returns a callable that is called when a render fails, to be used as:
        @client.on_render_fail()
        async def render_fail(event: RenderFailEvent):
        """

        @functools.wraps(func)
        async def wrapper(data: dict) -> Any:
            return await func(RenderFailEvent.parse_obj(data))

        self.socket.on("render_fail_json", wrapper)
        return wrapper

    def on_render_finish(self, func: Callable) -> Callable:
        r"""Returns a callable that is called when a render finishes, to be used as:
        @client.on_render_finish()
        async def render_finish(event: RenderFinishEvent):
        """

        @functools.wraps(func)
        async def wrapper(data: dict) -> Any:
            return await func(RenderFinishEvent.parse_obj(data))

        self.socket.on("render_finish_json", wrapper)
        return wrapper

    async def __aenter__(self) -> ordrClient:
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def _request(
        self, request_type: ClientRequestType, *args: Any, **kwargs: Any
    ) -> Any:
        if not self.socket.connected:
            await self.connect()
        if self._session is None:
            self._session = aiohttp.ClientSession()

        req: dict[str, Callable] = {
            "GET": self._session.get,
            "POST": self._session.post,
            "DELETE": self._session.delete,
            "PUT": self._session.put,
            "PATCH": self._session.patch,
        }

        async with self._limiter:
            async with req[request_type](*args, **kwargs) as resp:
                body = await resp.read()
                content_type = get_content_type(resp.headers.get("content-type", ""))
                if resp.status not in (200, 201):
                    json = orjson.loads(body)
                    error_code = json.get("errorCode", 0)
                    raise APIException(
                        resp.status,
                        json.get("message", ""),
                        ErrorCode(error_code),
                    )
                if content_type == "application/json":
                    return orjson.loads(body)
                if content_type == "text/html":
                    return body.decode("utf-8")
                raise APIException(415, "Unhandled Content Type", ErrorCode(0))

    async def get_skin(self, skin_id: int) -> SkinCompact:
        r"""Get custom skin information.

        :param skin_id: Skin ID
        :type skin_id: ``int``
        :raises: ``aiordr.exceptions.APIException``
        :return: Skin information
        :rtype: ``aiordr.models.skin.SkinCompact``
        """
        params = {"id": skin_id}
        json = await self._request(
            "GET",
            f"{self._base_url}/ordr/skins/custom",
            params=params,
        )
        return SkinCompact.parse_obj(json)

    async def get_skins(
        self, page: int = 1, page_size: int = 5, **kwargs: Any
    ) -> SkinsResponse:
        r"""Get custom skins.

        :param page: Page number
        :type page: ``int``
        :param page_size: Page size
        :type page_size: ``int``
        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *search* (``str``) --
                Optional, search query

        :raises: ``aiordr.exceptions.APIException``
        :return: Skins
        :rtype: ``aiordr.models.skins.SkinsResponse``
        """
        params = {
            "page": page,
            "pageSize": page_size,
        }
        add_param(params, kwargs, "search")
        json = await self._request(
            "GET",
            f"{self._base_url}/ordr/skins",
            params=params,
        )
        return SkinsResponse.parse_obj(json)

    async def get_render_list(
        self, page: int = 1, page_size: int = 5, **kwargs: Any
    ) -> RendersResponse:
        r"""Get render list.

        :param page: Page number
        :type page: ``int``
        :param page_size: Page size
        :type page_size: ``int``
        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *ordr_username* (``str``) --
                Optional, username of the user who ordered the render
            * *replay_username* (``str``) --
                Optional, username of the user from the replay
            * *render_id* (``int``) --
                Optional, ID of the render
            * *no_bots* (``bool``) --
                Optional, whether to exclude bot renders
            * *link* (``str``) --
                Optional, the path of a shortlink (e.g. pov8n for https://link.issou.best/pov8n)
            * *beatmapset_id* (``int``) --
                Optional, ID of the beatmapset

        :raises: ``aiordr.exceptions.APIException``
        :return: Renders
        :rtype: ``aiordr.models.renders.RendersResponse``
        """
        params = {
            "page": page,
            "pageSize": page_size,
        }
        add_param(params, kwargs, "ordr_username", "ordrUsername")
        add_param(params, kwargs, "replay_username", "replayUsername")
        add_param(params, kwargs, "render_id", "renderID")
        add_param(params, kwargs, "no_bots", "nobots")
        add_param(params, kwargs, "link")
        add_param(params, kwargs, "beatmapset_id", "beatmapsetid")
        json = await self._request(
            "GET",
            f"{self._base_url}/ordr/renders",
        )
        return RendersResponse.parse_obj(json)

    async def get_server_list(self) -> list[RenderServer]:
        r"""Get the list of available servers.


        :raises: ``aiordr.exceptions.APIException``
        :return: List of servers
        :rtype: ``list[aiordr.models.server.RenderServer]``
        """
        json = await self._request(
            "GET",
            f"{self._base_url}/servers",
        )
        return from_list(RenderServer.parse_obj, json.get("servers", []))

    async def get_server_online_count(self) -> int:
        r"""Get the number of online servers.


        :raises: ``aiordr.exceptions.APIException``
        :return: Number of online servers
        :rtype: ``int``
        """
        data = await self._request(
            "GET",
            f"{self._base_url}/servers/onlinecount",
        )
        try:
            return int(data)
        except ValueError:
            return 0

    async def create_render(
        self, username: str, skin: Union[str, int], **kwargs: Any
    ) -> RenderCreateResponse:
        r"""Create a render.

        :param username: Username of the user who ordered the render
        :type username: ``str``
        :param skin: Skin ID or name
        :type skin: ``Union[str, int]``
        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *replay_file* (``str``) --
                Optional, replay file
            * *replay_url* (``str``) --
                Optional, replay URL, used if replay_file is not provided
            * *render_options* (``aiordr.models.render.RenderOptions``) --
                Optional, render options
            * *custom_skin* (``bool``) --
                Optional, whether the provided skin is a custom skin ID (default: false)

        :raises: ``aiordr.exceptions.APIException``
        :raises: ``TypeError``
        :return: Render create response
        :rtype: ``aiordr.models.render.RenderCreateResponse``
        """

        if "replay_file" not in kwargs and "replay_url" not in kwargs:
            raise ValueError("Either replay_file or replay_url must be provided")

        data = {
            "username": username,
            "skin": skin,
        }
        if self._verification_key:
            data["verificationKey"] = self._verification_key

        if "render_options" not in kwargs:
            kwargs["render_options"] = RenderOptions()
        options: RenderOptions = kwargs["render_options"]
        if not isinstance(options, RenderOptions):
            raise TypeError("render_options must be a RenderOptions object")

        data.update(options.dict(exclude_defaults=True, by_alias=True))
        add_param(data, kwargs, "replay_file", "replayFile")
        add_param(data, kwargs, "replay_url", "replayURL")
        add_param(data, kwargs, "custom_skin", "customSkin")
        json = await self._request(
            "POST",
            f"{self._base_url}/ordr/renders",
            data=data,
        )
        return RenderCreateResponse.parse_obj(json)

    async def connect(self) -> None:
        r"""Connects to the websocket server.

        :return: None
        """
        await self.socket.connect(url=self._websocket_url)

    async def close(self) -> None:
        r"""Closes the client.

        :return: None
        """
        if self._session is not None:
            await self._session.close()
        await self.socket.close()
