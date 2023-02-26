"""
This module contains models for renders.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from .base import BaseModel

__all__ = (
    "RenderResolution",
    "RenderOptions",
    "Render",
    "RendersResponse",
    "RenderCreateResponse",
)


class RenderResolution(Enum):
    SD_480 = "720x480"
    SD_960 = "960x540"
    HD_720 = "1280x720"
    HD_1080 = "1920x1080"


class RenderOptions(BaseModel):
    resolution: RenderResolution = Field(default=RenderResolution.HD_720)
    global_volume: int = Field(alias="globalVolume", default=50)
    music_volume: int = Field(alias="musicVolume", default=50)
    hitsound_volume: int = Field(alias="hitsoundVolume", default=50)
    show_hit_error_meter: bool = Field(alias="showHitErrorMeter", default=True)
    show_unstable_rate: bool = Field(alias="showUnstableRate", default=True)
    show_score: bool = Field(alias="showScore", default=True)
    show_hp_bar: bool = Field(alias="showHPBar", default=True)
    show_combo_counter: bool = Field(alias="showComboCounter", default=True)
    show_pp_counter: bool = Field(alias="showPPCounter", default=True)
    show_key_overlay: bool = Field(alias="showKeyOverlay", default=True)
    show_scoreboard: bool = Field(alias="showScoreboard", default=True)
    show_borders: bool = Field(alias="showBorders", default=True)
    show_mods: bool = Field(alias="showMods", default=True)
    show_result_screen: bool = Field(alias="showResultScreen", default=True)
    use_skin_cursor: bool = Field(alias="useSkinCursor", default=True)
    use_skin_hitsounds: bool = Field(alias="useSkinHitsounds", default=True)
    use_beatmap_colors: bool = Field(alias="useBeatmapColors", default=True)
    cursor_scale_to_cs: bool = Field(alias="cursorScaleToCS", default=False)
    cursor_rainbow: bool = Field(alias="cursorRainbow", default=False)
    cursor_trail_glow: bool = Field(alias="cursorTrailGlow", default=False)
    draw_follow_points: bool = Field(alias="drawFollowPoints", default=True)
    draw_combo_numbers: bool = Field(alias="drawComboNumbers", default=True)
    cursor_size: float = Field(alias="cursorSize", default=1.0)
    cursor_trail: bool = Field(alias="cursorTrail", default=True)
    beat_scaling: bool = Field(alias="scaleToTheBeat", default=False)
    slider_merge: bool = Field(alias="sliderMerge", default=False)
    objects_rainbow: bool = Field(alias="objectsRainbow", default=False)
    flash_objects: bool = Field(alias="objectsFlashToTheBeat", default=False)
    use_slider_hitcircle_color: bool = Field(alias="useHitCircleColor", default=True)
    seizure_warning: bool = Field(alias="seizureWarning", default=False)
    load_storyboard: bool = Field(alias="loadStoryboard", default=True)
    load_video: bool = Field(alias="loadVideo", default=True)
    intro_bg_dim: int = Field(alias="introBGDim", default=0)
    ingame_bg_dim: int = Field(alias="inGameBGDim", default=75)
    break_bg_dim: int = Field(alias="breakBGDim", default=30)
    bg_parallax: bool = Field(alias="BGParallax", default=False)
    show_danser_logo: bool = Field(alias="showDanserLogo", default=True)
    skip_intro: bool = Field(alias="skip", default=True)
    cursor_ripples: bool = Field(alias="cursorRipples", default=False)
    slider_snaking_in: bool = Field(alias="sliderSnakingIn", default=True)
    slider_snaking_out: bool = Field(alias="sliderSnakingOut", default=True)
    show_hit_counter: bool = Field(alias="showHitCounter", default=False)
    show_avatars_on_scoreboard: bool = Field(
        alias="showAvatarsOnScoreboard",
        default=False,
    )
    show_aim_error_meter: bool = Field(alias="showAimErrorMeter", default=False)
    play_nightcore_samples: bool = Field(alias="playNightcoreSamples", default=True)


class Render(RenderOptions):
    id: int = Field(alias="renderID")
    date: datetime
    username: str
    progress: str
    renderer: str
    description: str
    title: str
    readable_date: str = Field(alias="readableDate")
    is_bot: bool = Field(alias="isBot")
    is_verified: bool = Field(alias="isVerified")
    replay_file_path: str = Field(alias="replayFilePath")
    video_url: str = Field(alias="videoUrl")
    map_link: str = Field(alias="mapLink")
    map_title: str = Field(alias="mapTitle")
    replay_difficulty: str = Field(alias="replayDifficulty")
    replay_username: str = Field(alias="replayUsername")
    map_id: int = Field(alias="mapID")
    need_to_redownload: bool = Field(alias="needToRedownload")
    skin: str
    has_cursor_middle: bool = Field(alias="hasCursorMiddle")
    motion_blur: bool = Field(alias="motionBlur960fps")
    render_start_time: datetime = Field(alias="renderStartTime")
    render_end_time: datetime = Field(alias="renderEndTime")
    upload_end_time: datetime = Field(alias="uploadEndTime")
    render_total_time: int = Field(alias="renderTotalTime")
    upload_total_time: int = Field(alias="uploadTotalTime")
    map_length: int = Field(alias="mapLength")
    replay_mods: str = Field(alias="replayMods")
    removed: bool


class RendersResponse(BaseModel):
    renders: list[Render]
    max_renders: int = Field(alias="maxRenders")


class RenderCreateResponse(BaseModel):
    message: str
    render_id: int = Field(alias="renderID")
