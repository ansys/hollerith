#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include "numpy/arrayobject.h"

#define NULL 0
#define DOUBLE_BUFFER_MAX_SIZE 30

#include "Python.h"
#include "pythoncapi_compat.h"

static void right_justify(char* output, int output_size, char* value, int value_size) {
  memset(output, ' ', output_size);
  int int_buffer_len = (int)strlen(value);
  int offset = output_size - int_buffer_len;
  strncpy(output + offset, value, int_buffer_len);
}

static PyObject* empty_string(int width) {
  static char buffer[200];
  memset(buffer, ' ', width);
  return PyUnicode_FromStringAndSize(buffer, width);
}

static PyObject* size_t_to_string(Py_ssize_t i, int width) {
  static char output_buffer[20];
  memset(output_buffer, 0, 20);
  static char int_buffer[21];
  memset(int_buffer, 0, 21);
  snprintf(int_buffer, width+1, "%lld", i);
  int int_buffer_len = (int)strlen(int_buffer);
  right_justify(output_buffer, width, int_buffer, int_buffer_len);
  return PyUnicode_FromStringAndSize(output_buffer, width);
}

static int is_whole(double d) {
  return ceil(d) == d;
}

static char* trimfront(char* input, int* num_trimmed) {
  int n = 0;
  while (isspace(input[0])) {
      ++input;
      ++n;
  }
  *num_trimmed = n;
  return input;
}

static void format_decimal_double(char* double_buffer, double d, int width) {
  static char big_buffer[DOUBLE_BUFFER_MAX_SIZE];
  memset(big_buffer, 0, DOUBLE_BUFFER_MAX_SIZE);

  // initially - leave at least enough space for period and sign
  int precision = width - 2;

  //declare variables used by trimming and truncating
  int num_trimmed, size;

  // attempt to fill the buffer with the initially chosen specifier
  sprintf(big_buffer, "%*.*g", width, precision, d);
  char* trimmed_buf = trimfront(big_buffer, &num_trimmed);

  // if the size is bigger than width, keep trying and reduce the precision in a loop
  // give up after 6 tries.
  int MAX_TRIES=6;
  int try_index = 0;
  while (1) {
    size = strlen(trimmed_buf);
    if (size <= width) {
      break;
    }
    if (
      (++try_index == MAX_TRIES) /* something went wrong if we tried this many times*/ ||
      (precision == 0)           /* can't reduce the precision any further          */
      ) {
      strcpy(double_buffer, "INVALID");
      return;
    }

    precision = precision - (size - width);
    memset(big_buffer, '\0', DOUBLE_BUFFER_MAX_SIZE);
    sprintf(big_buffer, "%*.*g", width, precision, d);
    trimmed_buf = trimfront(big_buffer, &num_trimmed);
  }

  // We exited the loop - so the buffer fits!
  // Copy it to the output, using a length that accounts for
  // +1 (null terminator)
  strncpy(double_buffer, trimmed_buf, size+1);
}

static void format_whole_double(char* double_buffer, double d, int width) {
  // first check to see if %.1f fits in width
  static char big_buffer[DOUBLE_BUFFER_MAX_SIZE];
  memset(big_buffer, 0, DOUBLE_BUFFER_MAX_SIZE);
  sprintf(big_buffer, "%.1f", d);
  int size = (int)strnlen(big_buffer, DOUBLE_BUFFER_MAX_SIZE);
  if (size <= width) {
    // copy it (including null terminator) and exit
    strncpy(double_buffer, big_buffer, size+1);
    return;
  }

  // %.1f does not fit in width - fallback to format_decimal_double
  format_decimal_double(double_buffer, d, width);
}

/**
 * @brief Write a double into the buffer with the given width.
 *        HERE BE DRAGONS
 *
 * @param double_buffer output buffer to write to
 * @param d value to write
 * @param width number of characters to use
 */
static void format_double(char* double_buffer, double d, int width) {
  if (is_whole(d)) {
    format_whole_double(double_buffer, d, width);
  } else {
    format_decimal_double(double_buffer, d, width);
  }
}

static PyObject* double_to_string(double d, int width) {
  static char output_buffer[20];
  memset(output_buffer, 0, 20);
  static char double_buffer[21];
  memset(double_buffer, 0, 21);
  format_double(double_buffer, d, width);
  int double_buffer_len = (int)strlen(double_buffer);
  right_justify(output_buffer, width, double_buffer, double_buffer_len);
  return PyUnicode_FromStringAndSize(output_buffer, width);
}

static int is_null(PyObject* value, PyObject* check_null) {
  PyObject* checknull_result = PyObject_CallOneArg(check_null, value);
  int result = PyObject_IsTrue(checknull_result);
  Py_DECREF(checknull_result);
  return result;
}

static PyObject* handle_null(PyObject* value, PyObject* check_null, int width) {
  if (!is_null(value, check_null)) {
    return NULL;
  }
  return empty_string(width);
}

static PyObject* handle_float(PyObject* value, int width) {
  //numpy floats derive from PyFloat
  if (!PyFloat_Check(value)) {
    return NULL;
  }
  assert(width <= 20); //crash if the width for a float field is more than 20.
  double double_value = PyFloat_AS_DOUBLE(value);
  return double_to_string(double_value, width);
}

static PyObject* handle_int(PyObject* value, int width) {
  Py_ssize_t int_value;
  if (PyLong_Check(value)) {
    int_value = PyLong_AsSsize_t(value);
  } else {
    PyObject* int_func = PyObject_GetAttrString(value, "__int__");
    if (int_func == NULL) {
      return NULL;
    }
    PyObject* result = PyObject_CallNoArgs(int_func);
    Py_DECREF(int_func);
    if (result == NULL) {
      return NULL;
    }
    int_value = PyLong_AsSsize_t(result);
    Py_DECREF(result);
  }
  return size_t_to_string(int_value, width);
}

static PyObject* pad_right(char* buffer, int width, int size) {
  static char value[200];
  memset(value, ' ', 200);
  strncpy(value, buffer, size);
  PyObject* result = PyUnicode_DecodeUTF8(value, width, NULL);
  return result;
}

static PyObject* handle_string(PyObject* value, int width) {
  if (!PyUnicode_CheckExact(value)) {
    return NULL;
  }

  if (-1 == PyUnicode_READY(value)) {
    return NULL;
  }

  Py_ssize_t size;
  char* buffer = PyUnicode_AsUTF8AndSize(value, &size);
  //negative means we need to add padding, non-negative means we need to truncate
  int difference = size - width;
  if (size < width) {
    return pad_right(buffer, width, size);
  }
  else /*difference >= 0*/ {
    //truncate even if the sizes match so that we get utf-8 buffers always.
    return PyUnicode_DecodeUTF8(buffer, width, NULL);
  }
}

static PyObject* float_to_string(PyObject* value, PyObject* check_null, int width) {
  PyObject* result = handle_null(value, check_null, width);
  if (result == NULL) {
    result = handle_float(value, width);
  }
  return result;
}

static PyObject* int_to_string(PyObject* value, PyObject* check_null, int width) {
  PyObject* result = handle_null(value, check_null, width);
  if (result == NULL) {
    result = handle_int(value, width);
  }
  return result;
}

static PyObject* string_to_string(PyObject* value, PyObject* check_null, int width) {
  PyObject* result = handle_null(value, check_null, width);
  if (result == NULL) {
    result = handle_string(value, width);
  }
  return result;
}

/**
 * @brief writes string using write.
 *
 * @param write callable object
 * @param string value to write
 * @returns int error code, 0 on error, 1 on success
 */
static int write_string(PyObject* write, PyObject* string) {
  PyObject* result = PyObject_CallOneArg(write, string);
  if (result == NULL) {
    return 0;
  }

  Py_DECREF(result);
  return 1;
}

/**
 * @brief validates the inputs, width, write and check_null
 * @return int 1 on success, something else on failure
 */
static int validate_inputs(PyObject* write, PyObject* check_null, int width) {
  if (width < 1) {
    return 0;
  }

  if (write == NULL || check_null == NULL) {
    return -1;
  }
  return 1;
}

int write_float_value(PyObject* write, PyObject* check_null, PyObject* value, int width) {
  int valid = validate_inputs(write, check_null, width); // TODO put the variable in the if expression for brevity
  if (valid != 1) {
    return valid;
  }

  PyObject* arg = float_to_string(value, check_null, width);
  if (arg == NULL) {
    return -2;
  }

  if (0 == write_string(write, arg)) {
    Py_DECREF(arg);
    return -3;
  }

  Py_DECREF(arg);
  return 1;
}

int write_int_value(PyObject* write, PyObject* check_null, PyObject* value, int width) {
  int valid = validate_inputs(write, check_null, width);
  if (valid != 1) {
    return valid;
  }

  PyObject* arg = int_to_string(value, check_null, width);
  if (arg == NULL) {
    return -2;
  }

  if (0 == write_string(write, arg)) {
    Py_DECREF(arg);
    return -3;
  }

  Py_DECREF(arg);
  return 1;
}

int write_string_value(PyObject* write, PyObject* check_null, PyObject* value, int width) {
  int valid = validate_inputs(write, check_null, width);
  if (valid != 1) {
    return valid;
  }

  PyObject* arg = string_to_string(value, check_null, width);
  if (arg == NULL) {
    return -2;
  }

  if (0 == write_string(write, arg)) {
    Py_DECREF(arg);
    return -3;
  }

  Py_DECREF(arg);
  return 1;
}

int write_null_value(PyObject* write, int width) {
  if (width < 1) {
    return 0;
  }

  if (write == NULL) {
    return -1;
  }
  PyObject* arg = empty_string(width);
  if (0 == write_string(write, arg)) {
    Py_DECREF(arg);
    return -3;
  }

  Py_DECREF(arg);
  return 1;
}
