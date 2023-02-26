:orphan:

.. _quickstart:

.. currentmodule:: aiordr

Quickstart
============


Installing
----------

**Python 3.9 or higher is required**

To install the library, simply run the following commands

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U aiordr

    # Windows
    py -3 -m pip install -U aiordr


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/NiceAesth/aiordr
    $ cd aiordr
    $ python3 -m pip install -U .


API Example
-----------

.. code:: py

    import aiordr
    import asyncio


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

More examples can be found in the `repository <https://github.com/NiceAesth/aiordr/tree/master/examples>`__
