#################
Developer's Guide
#################


.. toctree::
    :maxdepth: 2

    events
    frontend
    jsonrpc
    implementing_a_card
    implementation_notes


Running the Test Suite
======================

Running the test suite can be accomplished by running

    ``trial cardboard``

(or via your test runner of choice). In addition, all the integration tests are
kept inside the :mod:`cardboard.integration_tests` package, so restricting to
only the integration tests can be accomplished with

    ``trial cardboard.integration_tests``

or omitting them via

    ``trial cardboard.tests``
