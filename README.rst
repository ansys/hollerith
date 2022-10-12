Project Overview
----------------
Hollerith is a small python library that supports fixed-width formatting of some value types and
tables. It is named after Herman Hollerith, the inventor of punch cards.


Installation
------------
Include installation directions.  Note that this README will be
included in your PyPI package, so be sure to include ``pip``
directions along with developer installation directions.  For example.

Install hollerith with:

.. code::

   pip install hollerith

Alternatively, clone and install in development mode with:

.. code::

   git clone https://github.com/pyansys/hollerith
   cd hollerith
   pip install .

Documentation
-------------
Include a link to the full sphinx documentation.  For example `PyAnsys <https://docs.pyansys.com/>`_


Usage
-----
It's best to provide a sample code or even a figure demonstrating the usage of your library.  For example:

.. code:: python

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
