..
   Just reuse the root readme to avoid duplicating the documentation.
   Provide any documentation specific to your online documentation
   here.

.. include:: ../../README.rst

.. toctree::
   :hidden:
   :maxdepth: 3

   class_documentation


Code Examples
~~~~~~~~~~~~~
Here's a quick preview for how Python code looks using
``hollerith```.  For more examples, click the links at the
top of the page to see function, method, and class documentation.


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

