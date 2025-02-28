Hollerith
=========
|pyansys| |python| |pypi| |GH-CI| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/hollerith?logo=pypi
   :target: https://pypi.org/project/hollerith/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/hollerith.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/hollerith
   :alt: PyPI

.. |GH-CI| image:: https://github.com/ansys/hollerith/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/hollerith/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

Hollerith is a small python library that supports fixed-width formatting of some value types and
tables. It is named after Herman Hollerith, the inventor of punch cards.

Install the package
-------------------

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing hollerith in user mode, make sure you have the latest version of
`pip <https://pypi.org/project/pip/>`_ with:

.. code:: bash

   python -m pip install -U pip

Then, install hollerith with:

.. code::

   pip install hollerith

Install in developer mode
^^^^^^^^^^^^^^^^^^^^^^^^^

Installing hollerith in developer mode allows
you to modify the source and enhance it.

.. note::
   
    Before contributing to the project, ensure that you are thoroughly familiar
    with the `PyAnsys Developer's Guide <https://dev.docs.pyansys.com/>`_.
    
To install hollerith in developer mode, perform these steps:

.. code::

   git clone https://github.com/ansys/hollerith
   cd hollerith
   pip install .

Install in offline mode
^^^^^^^^^^^^^^^^^^^^^^^

If you lack an internet connection on your installation machine,
you should install hollerith by downloading the wheelhouse
archive from the `Releases Page <https://github.com/ansys/hollerith/releases>`_ for your
corresponding machine architecture.

Each wheelhouse archive contains all the Python wheels necessary to install hollerith from scratch on Windows,
Linux, and MacOS from Python 3.8 to 3.11.

Documentation
-------------
In addition to installation information, the `hollerith <https://hollerith.docs.pyansys.com/>`_ 
documentation provides information on API reference.

Usage
-----
Example:

.. code-block:: pycon

   >>> import io
   >>> import hollerith as holler
   >>> s = io.StringIO()
   >>> holler.write_float(s, 1.2099, 10)
   >>> holler.write_int(s, 2803, 10)
   >>> holler.write_float(s, float("nan"), 10)
   >>> holler.write_int(s, 0, 10)
   >>> s.getvalue()
   '    1.2099      2803                   0'

License
-------
``hollerith`` is licensed under the MIT license.
The full license can be found in the root directory of the repository, 
see `License <https://github.com/ansys/hollerith/blob/main/LICENSE>`_.
