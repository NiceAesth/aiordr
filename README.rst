aiordr
======

|Python| |pypi| |pre-commit.ci status| |rtd| |pytest| |mypy| |codacy|

Simple and fast asynchronous library for the o!rdr API.


Features
--------

- Support for modern async syntax (async with)
- Event decorators
- Rate limit handling
- Easy to use


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


Contributing
------------

Please read the `CONTRIBUTING.rst <.github/CONTRIBUTING.rst>`__ to learn how to contribute to aiordr!


Acknowledgments
---------------

-  `discord.py <https://github.com/Rapptz/discord.py>`__
   for README formatting
-  `aiosu <https://github.com/NiceAesth/aiosu>`__
   sister library for the osu! API


.. |Python| image:: https://img.shields.io/pypi/pyversions/aiordr.svg
    :target: https://pypi.python.org/pypi/aiordr
    :alt: Python version info
.. |pypi| image:: https://img.shields.io/pypi/v/aiordr.svg
    :target: https://pypi.python.org/pypi/aiordr
    :alt: PyPI version info
.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/NiceAesth/aiordr/master.svg
    :target: https://results.pre-commit.ci/latest/github/NiceAesth/aiordr/master
    :alt: pre-commit.ci status
.. |pytest| image:: https://github.com/NiceAesth/aiordr/actions/workflows/pytest.yml/badge.svg
    :target: https://github.com/NiceAesth/aiordr/actions/workflows/pytest.yml
    :alt: pytest Status
.. |mypy| image:: https://github.com/NiceAesth/aiordr/actions/workflows/mypy.yml/badge.svg
    :target: https://github.com/NiceAesth/aiordr/actions/workflows/mypy.yml
    :alt: mypy Status
.. |rtd| image:: https://readthedocs.org/projects/aiordr/badge/?version=latest
    :target: https://aiordr.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |codacy| image:: https://app.codacy.com/project/badge/Grade/4778d5ee1dc84469ad6a43a6f961c0eb
    :target: https://www.codacy.com/gh/NiceAesth/aiordr/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NiceAesth/aiordr&amp;utm_campaign=Badge_Grade
    :alt: Codacy Status
