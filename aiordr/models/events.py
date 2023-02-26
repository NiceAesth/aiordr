"""
This module contains models for websocket events.
"""
from __future__ import annotations

from pydantic import Field

from .base import BaseModel
from .errorcode import ErrorCode

__all__ = (
    "RenderBaseEvent",
    "RenderAddEvent",
    "RenderProgressEvent",
    "RenderFinishEvent",
    "RenderFailEvent",
)


class RenderBaseEvent(BaseModel):
    render_id: int = Field(alias="renderID")


class RenderAddEvent(RenderBaseEvent):
    pass


class RenderProgressEvent(RenderBaseEvent):
    username: str
    """Username of the user who requested the render."""
    progress: str
    """Status text of the render process."""
    renderer: str
    """Name of the render server."""
    description: str
    """Video description."""


class RenderFinishEvent(RenderBaseEvent):
    video_url: str = Field(alias="videoUrl")


class RenderFailEvent(RenderBaseEvent):
    error_message: str = Field(alias="errorMessage")
    error_code: ErrorCode = Field(alias="errorCode")
