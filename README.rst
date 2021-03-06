=======================
FIT file I/O for Python
=======================

The Flexible and Interoperable Data Transfer (FIT) protocol is a format designed
specifically for the storing and sharing of data that originates from sport,
fitness and health devices. It is specifically designed to be compact,
interoperable and extensible. This document will describe the FIT file structure
and interpretation.

The FIT protocol defines a set of data storage templates (FIT messages) that can
be used to store information such as user profiles and activity data in files.
Any FIT-compliant device can interpret a FIT file from any other FIT-compliant
device.

How-To
------
.. code:: python

    from fit import FitFile
    from fit.files.activity import ActivityFile
    from fit.messages.common import FileCreator


    fin = FitFile.open("path/to/filename.fit")
    for msg in fin:
        print msg

    with FitFile.open("path/to/copy.fit", mode="w") as fout:
        fout.copy(fin)

    fnew = ActivityFile.create("path/to/new.fit")
    fnew.append(FileCreator(software_version=666))
    fnew.write()
    fnew.close()

TODO
----
* Component fields
* Accumulated fields
* Tests (you can submit me some cool examples)
* Entry Points for external extensions
* Convertible types
* ...
