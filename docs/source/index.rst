Welcome to aiordr
=================

aiordr is an easy-to-use asynchronous wrapper for the osu! API

**Features:**

- Support for modern async syntax (async with)
- Event decorators
- Rate limit handling
- Easy to use

Getting started
---------------

If you are new to this library, you should familiarize yourself with the following pages:

- **First steps:** :doc:`quickstart`
- **Examples:** Examples can be found in the `repository <https://github.com/NiceAesth/aiordr/tree/master/examples>`__

Getting help
------------

If you need assistance, you should look here:

- Try the :ref:`index <genindex>` or :ref:`searching <search>`
- Contact me on `Discord <https://discord.gg/ufHV3T3UPD>`_
- Report bugs in the `issue tracker <https://github.com/NiceAesth/aiordr/issues>`_

Breaking changes
----------------

**v0.2.2:** The `close()` method of the client is now named `aclose()` as per naming conventions for asynchronous methods. The old method is still available with a deprecation warning, but will be removed on 2024-03-01.

**v0.1.0:** The library now uses *Pydantic v2*. This means that the following changes have occured:

- The *dict* method has been renamed to *model_dump*
- The *json* method has been renamed to *model_dump_json*
- The *parse_obj* method has been renamed to *model_validate*
- The *parse_raw* method has been renamed to *model_validate_json*
- The *parse_file* method has been renamed to *model_validate_file*

Note: The old methods are still available with a deprecation warning, but will be removed in Pydantic v3.

Client
------

Documentation for the API client can be found below.

.. toctree::
   :maxdepth: 1
   :glob:

   client.rst

Models
-------

Documentation for `aiordr` types can be found below.

.. toctree::
   :maxdepth: 1

   models/index.rst

Library Classes
---------------

Documentation for `aiordr` classes can be found below.

.. toctree::
   :maxdepth: 1

   library/index.rst
