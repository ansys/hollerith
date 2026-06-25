# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cython
from libc.stdlib cimport malloc, free
from cpython.exc cimport PyErr_Occurred

import numpy as np  # Python-level symbols of numpy

cimport numpy as np  # C-level symbols of numpy

from pandas._libs.missing import checknull

# Numpy must be initialized from C or Cython to avoid segfaults
np.import_array()

import typing

cdef extern from 'writer.h':
    int write_float_value(object write, object check_null, object value, int width)
    int write_int_value(object write, object check_null, object value, int width)
    int write_string_value(object write, object check_null, object value, int width)
    int write_null_value(object write, int width)

cdef int throw_write_error(int code) except -1:
    """Translate a C-level error code into a Python exception.

    Returns 0 on success (code == 1) or raises.  Declaring the return type as
    ``int`` with ``except -1`` means Cython will check ``PyErr_Occurred()``
    whenever this function returns -1, so a *pre-existing* C exception (e.g.
    the ``SystemError`` set by ``validate_inputs`` when ``write`` is not
    callable) is propagated correctly instead of being replaced by the generic
    hollerith ``Exception``.  This became critical in Python 3.14, which no
    longer raises ``SystemError`` on its own when Python code is called while
    an exception is already pending.
    """
    if code == 1:
        return 0
    # If the C code already set a Python exception (e.g. SystemError for a
    # non-callable write attribute), signal Cython to propagate it by
    # returning the -1 sentinel.  Cython will then call PyErr_Occurred()
    # and propagate the existing exception without us constructing a new one.
    if PyErr_Occurred():
        return -1
    raise Exception(f"error in hollerith: {code}")

cpdef write_float_to_buffer(buffer, double value, int width):
    """Writes a string representing the float ``value`` to ``buffer`` within the given ``width``, right justified.

        Parameters
        ----------
        buffer :
            Buffer to write to - it could be a file or a StringIO object, for example. The only
            requirement is that it must contain a write attribute that is callable with a single
            string argument.
        value : float
            Float to write.
        width : int
            The number of characters to write

        Examples
        --------

        >>> import io
        >>> import hollerith as holler
        >>> buffer = io.StringIO()
        >>> holler.write_float(buffer, 1.0, 16)
        >>> print(buffer.getvalue())
            '             1.0'
    """
    output: int = write_float_value(buffer.write, checknull, value, width)
    throw_write_error(output)

cpdef write_int_to_buffer(buffer, int value, int width):
    """Writes a string representing the int ``value`` to ``buffer`` within the given ``width``, right justified.

        Parameters
        ----------
        buffer :
            Buffer to write to - it could be a file or a StringIO object, for example. The only
            requirement is that it must contain a write attribute that is callable with a single
            string argument.
        value : int
            Integer to write. This could also be a numpy.int32
        width : int
            The number of characters to write

        Examples
        --------

        >>> import io
        >>> import hollerith as holler
        >>> buffer = io.StringIO()
        >>> holler.write_int(buffer, 145, 16)
        >>> print(buffer.getvalue())
            '             145'
    """
    output: int = write_int_value(buffer.write, checknull, value, width)
    throw_write_error(output)

cpdef write_string_to_buffer(buffer, str value, int width):
    """Writes a string representing the string ``value`` to ``buffer`` within the given ``width``, left justified.

        Parameters
        ----------
        buffer :
            Buffer to write to - it could be a file or a StringIO object, for example. The only
            requirement is that it must contain a write attribute that is callable with a single
            string argument.
        value : string
            String to write.
        width : int
            The number of characters to write

        Examples
        --------

        >>> import io
        >>> import hollerith as holler
        >>> buffer = io.StringIO()
        >>> holler.write_string(s, "hello", 16)
        >>> print(buffer.getvalue())
            'hello           '
    """
    output: int = write_string_value(buffer.write, checknull, value, width)
    throw_write_error(output)

cpdef write_null_to_buffer(buffer, int width):
    """Writes ``width`` space characters to ``buffer``

        Parameters
        ----------
        buffer :
            Buffer to write to - it could be a file or a StringIO object, for example. The only
            requirement is that it must contain a write attribute that is callable with a single
            string argument.
        width : int
            The number of spaces to write

        Examples
        --------

        >>> import io
        >>> import hollerith as holler
        >>> buffer = io.StringIO()
        >>> holler.write_spaces(buffer, 16)
        >>> print(buffer.getvalue())
            '                '
    """
    output: int = write_null_value(buffer.write, width)
    throw_write_error(output)

cdef struct s_field:
    int field_type #0-int, 1-float, 2-string, 3-null
    int field_width

cdef struct s_fields:
    int size
    s_field* arr

cdef int get_overall_width(fields: s_fields):
    cdef int width = 0
    cdef int i
    for i in range(fields.size):
        width += fields.arr[i].field_width
    return width

cdef s_fields convert_field_spec(spec: typing.List):
    """
    This function allocates space for the s_fields.arr using `malloc`.
    caller  is responsible for freeing it using `free`.
    """
    cdef s_fields fields
    cdef int width
    cdef int i
    fields.size = len(spec)
    fields.arr = <s_field*>malloc(len(spec)*cython.sizeof(s_field))
    if fields.arr is NULL:
        raise MemoryError()
    for i in range(len(spec)):
        item = spec[i]
        typ: type = item.type
        width = item.width
        fields.arr[i].field_width = width
        if typ == int:
            fields.arr[i].field_type = 0
        elif typ == float:
            fields.arr[i].field_type = 1
        elif typ == str:
            fields.arr[i].field_type = 2
        elif typ == None:
            fields.arr[i].field_type = 3
    return fields


cdef write_row(write, spec: s_fields, np.ndarray[object, ndim=1] row_arr):
    cdef int i
    cdef int write_output
    cdef int field_width
    cdef int field_type
    for i in range(spec.size):
        field_type = spec.arr[i].field_type
        field_width = spec.arr[i].field_width
        value = row_arr[i]
        if field_type == 0:
            write_output = write_int_value(write, checknull, value, field_width)
        elif field_type == 1:
            write_output = write_float_value(write, checknull, value, field_width)
        elif field_type == 2:
            write_output = write_string_value(write, checknull, value, field_width)
        elif field_type == 3:
            write_output = write_null_value(write, field_width)

        throw_write_error(write_output)

cpdef write_numpy_table(buffer, spec: typing.List, int numrows, np.ndarray[object, ndim=2] arr):
    """
        Write 2d numpy array to buffer with fixed width columns

        Parameters
        ----------
        buffer :
            Buffer to write to - it could be a file or a StringIO object, for example. The only
            requirement is that it must contain a write attribute that is callable with a single
            string argument.
        spec : List[hollerith.Field]
            Specification of the table. Must be the same length as the number of columns in `table`.
        numrows : int
            The number of rows to write. This might be larger than the length of `table`.
            If so, append with empty lines with the right size.
        arr : np.ndarray[object, ndim=2]
            2D array to write.

    """
    # when dealing with this numpy array - assume that all the values are object
    write: typing.Callable = buffer.write
    cdef int num_arr_rows = arr.shape[0]
    cdef int num_arr_cols = arr.shape[1]
    cdef int index
    if len(spec) != num_arr_cols:
        raise RuntimeError("spec does not match array")

    fields = convert_field_spec(spec)

    full_width = get_overall_width(fields)
    try:
        for index in np.arange(numrows):
            if index > 0:
                write("\n")
            if index >= num_arr_rows:
                output: int = write_null_value(write, full_width)
                throw_write_error(output)
            else:
                write_row(write, fields, arr[index])
    finally:
        free(fields.arr)
