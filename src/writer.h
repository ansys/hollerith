#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "Python.h"


/**
 * @brief writes a float
 *
 * @param write callable to write - io.StringIO().write
 * @param check_null callable object - pandas._libs.missing.checknull
 * @param value thing to write
 * @param width amount of characters to write
 * @return ** 1 on success, 0 on failure
 * @remark this function runs under the GIL - it is not threadsafe - for performance static string buffers are used
 */
int write_float_value(PyObject* write, PyObject* check_null, PyObject* value, int width);

/**
 * @brief writes a int
 *
 * @param write callable to write - io.StringIO().write
 * @param check_null callable object - pandas._libs.missing.checknull
 * @param value thing to write
 * @param width amount of characters to write
 * @return ** 1 on success, 0 on failure
 * @remark this function runs under the GIL - it is not threadsafe - for performance static string buffers are used
 */
int write_int_value(PyObject* write, PyObject* check_null, PyObject* value, int width);

/**
 * @brief writes a string
 *
 * @param write callable to write - io.StringIO().write
 * @param check_null callable object - pandas._libs.missing.checknull
 * @param value thing to write
 * @param width amount of characters to write
 * @return ** 1 on success, 0 on failure
 * @remark this function runs under the GIL - it is not threadsafe - for performance static string buffers are used
 */
int write_string_value(PyObject* write, PyObject* check_null, PyObject* value, int width);

/**
 * @brief writes spaces
 *
 * @param write callable to write - io.StringIO().write
 * @param width amount of characters to write
 * @return ** 1 on success, 0 on failure
 * @remark this function runs under the GIL - it is not threadsafe - for performance static string buffers are used
 */
int write_null_value(PyObject* write, int width);
