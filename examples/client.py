from __future__ import annotations

import asyncio

import aiordr


async def main():
    client = aiordr.ordrClient(verification_key="verylongstring")

    await client.create_render(
        "username",
        "YUGEN",
        replay_url="https://url.to.replay",
    )

    @client.on_render_added
    async def on_render_added(event: aiordr.models.RenderAddEvent) -> None:
        print(event)

    @client.on_render_progress
    async def on_render_progress(event: aiordr.models.RenderProgressEvent) -> None:
        print(event)

    @client.on_render_fail
    async def on_render_fail(event: aiordr.models.RenderFailEvent) -> None:
        print(event)

    @client.on_render_finish
    async def on_render_finish(event: aiordr.models.RenderFinishEvent) -> None:
        print(event)


if __name__ == "__main__":
    asyncio.run(main())
