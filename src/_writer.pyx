# cython: language_level=3
# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False
# cython: embedsignature=True

import cython
from libc.stdlib cimport malloc, free

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

cdef throw_write_error(code: int):
    if code == 1:
        return
    # TODO - raise the error in C?
    #      - or return an error code with a more useful message?
    raise Exception(f"error in hollerith: {code}")

cpdef write_float_to_buffer(buffer, value, width: int):
    """Writes a string representing the float `value` to `buffer` within the given `width`, and right justified.

    Parameters
    ----------
    buffer : buffer
        Buffer object
    value : np.ndarray?
        values to write
    width : int
        Width
    """
    output: int = write_float_value(buffer.write, checknull, value, width)
    throw_write_error(output)

cpdef write_int_to_buffer(buffer, value, width: int):
    """
    Writes a string representing the float `value` to `buffer` within the given `width`, right justified.
    """
    output: int = write_int_value(buffer.write, checknull, value, width)
    throw_write_error(output)

cpdef write_string_to_buffer(buffer, value, width: int):
    """Writes a string representing the float `value` to `buffer` within the given `width`, left justified."""
    output: int = write_string_value(buffer.write, checknull, value, width)
    throw_write_error(output)

cpdef write_null_to_buffer(buffer, width: int):
    """Writes `width` space characters to the buffer"""
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

cpdef write_numpy_table(buffer, spec: typing.List, numrows: int, np.ndarray[object, ndim=2] arr):
    """
    Write numpy table to buffer

    buffer: buffer to write to - it could be a file or a StringIO object
    spec: specification of the table column types and widths
    numrows: int
        the number of rows to write. This might be larger than the size of the numpy
        array suggests, if so, append with empty lines with the right size.
    arr: 2d numpy array of the table data
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
