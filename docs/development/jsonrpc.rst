****************
The JSON RPC API
****************

If you're looking to write a frontend for Cardboard, you'll need to be familiar
with the JSON RPC call and response API it uses.

.. sidebar:: JSON, JSON RPC, and JSON Schema

    If you're completely unfamiliar with JSON, JSON RPC, or JSON Schema, don't
    worry too much. By design, they're all fairly simple.

    You should be somewhat familiar with the :mod:`json` module in the Python
    standard library. For the rest, if you try to carefully follow the format
    of the method calls below, you shouldn't need to know much more. If you're
    not using Python, whatever language you're using likely has a JSON library
    written for it.
    
    If you insist on knowing more, you can take a quick glance at the 
    official specification for `JSON RPC 2.0 <http://jsonrpc.org/spec.html>`__,
    or the official specification for `JSON Schema Draft 3
    <http://tools.ietf.org/html/draft-zyp-json-schema-03>`__.

Communication with Cardboard involves listening for and responding to requests
from the game engine. The types of requests and responses are divided into a
number of different namespaces.

.. tip::

    Each request and response object below is described by a JSON Schema
    object.

Namespaces
==========

Game
----
