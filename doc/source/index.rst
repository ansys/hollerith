..
   Just reuse the root readme to avoid duplicating the documentation.
   Provide any documentation specific to your online documentation
   here.

.. include:: ../../README.rst

.. toctree::
   :hidden:
   :maxdepth: 3

   api_reference


Code Examples
~~~~~~~~~~~~~
Here's a quick preview for how Python code looks using ``hollerith``.


Rendered Python Code
--------------------

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

API Reference
~~~~~~~~~~~~~
To see a full API reference, see :ref:`ref_api_reference`
