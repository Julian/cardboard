=================
Developer's Guide
=================


Running the Test Suite
----------------------

Running the test suite can be accomplished by running

    trial cardboard

(or via your test runner of choice). In addition, all the integration tests are
kept inside the `cardboard/integration_tests` package, so restricting to only
the integration tests can be accomplished with

    trial cardboard.integration_tests

or omitting them via

    trial cardboard.tests


Game Notes
----------

What follows are a few notes related to the implementation of the M:TG rules.
In general, (I hope) they shouldn't be too noticeable during gameplay.


Bizarre Cards
^^^^^^^^^^^^^

The following cards break stuff, either by not following The Rules or by just
plain doing strange things in their characteristics. There may be more of each
oddity, I just picked the first one alphabetically.

* Architects of Will

It's type line reads "Artifact Creature -- Human Wizard", flaunting its
blatant disregard for rule 205.3c.

* Seeds of Strength

Wins a prize for having the same exact ability multiple times.
Besides messing with my table schema, this seems like a usability fail.

* Mishra's Factory

Simultaneously a rare and an uncommon in the same set.
