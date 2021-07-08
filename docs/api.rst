.. currentmodule:: pnwkit

**************
API Reference
**************

pnwkit
~~~~~~~

.. autodata:: pnwkit.pnwkit

An instance of :class:`SyncKit` for synchronous interactions with the API.

.. note::

    All methods of this instance can be accessed from the root pnwkit module. I.e. `pnwkit.alliance_query` as opposed to `pnwkit.pnwkit.alliance_query`.

async_pnwit
~~~~~~~~~~~~

.. autodata:: pnwkit.async_pnwkit

An instance of :class:`AsyncKit` for asynchronous interactions with the API.

.. note::

    All methods of this instance can be accessed from the root pnwkit module with prefix `async_`. I.e. `pnwkit.async_alliance_query` as opposed to `pnwkit.async_pnwkit.alliance_query`.

set_key
~~~~~~~~

.. autofunction:: pnwkit.set_key

Kit
~~~~

.. autoclass:: pnwkit.core.Kit
    :members:

SyncKit
~~~~~~~~
.. attributetable:: pnwkit.sync.SyncKit

.. autoclass:: pnwkit.sync.SyncKit
    :members:

AsyncKit
~~~~~~~~~
.. attributetable:: pnwkit.async_.AsyncKit

.. autoclass:: pnwkit.async_.AsyncKit
    :members: