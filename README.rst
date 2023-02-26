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
       async def on_render_added(data: dict) -> None:
           print(data)

       @client.on_render_progress
       async def on_render_progress(data: dict) -> None:
           print(data)

       @client.on_render_fail
       async def on_render_fail(data: dict) -> None:
           print(data)

       @client.on_render_finish
       async def on_render_finish(data: dict) -> None:
           print(data)


   if __name__ == "__main__":
       asyncio.run(main())


Contributing
------------

Please read the `CONTRIBUTING.rst <.github/CONTRIBUTING.rst>`__ to learn how to contribute to aiordr!


Acknowledgments
---------------

-  `discord.py <https://github.com/Rapptz/discord.py>`__
   for README formatting
- `aiosu <https://github.com/NiceAesth/aiosu>`__
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
.. |codacy| image:: https://app.codacy.com/project/badge/Grade/9bf211d7e29546dc99cc0b1a3d89b291
    :target: https://www.codacy.com/gh/NiceAesth/aiosu/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NiceAesth/aiosu&amp;utm_campaign=Badge_Grade
    :alt: Codacy Status
