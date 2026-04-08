# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

import io
import typing

import hollerith as holler


def write_field(
    buf: typing.IO[typing.AnyStr], field_type: type, value: typing.Any, width: int
) -> None:
    if field_type is None:
        holler.write_spaces(buf, width)
    elif field_type is str:
        holler.write_string(buf, value, width)
    elif field_type is int:
        holler.write_int(buf, value, width)
    elif field_type is float:
        holler.write_float(buf, value, width)


def _get_field_value(fields: typing.List[holler.Field], values: typing.List) -> str:
    s = io.StringIO()
    [write_field(s, field.type, value, field.width) for field, value in zip(fields, values)]
    return s.getvalue()


def test_field_values_int_string():
    """Test integer and string field values"""
    spec = [holler.Field(int, 10), holler.Field(str, 10)]
    result = _get_field_value(spec, [1, "hello"])
    assert result == "         1hello     "


def test_field_values_int_float_string():
    spec = [holler.Field(int, 10), holler.Field(float, 10), holler.Field(str, 10)]
    result = _get_field_value(spec, [1, 2.0, "hello"])
    assert result == "         1       2.0hello     "


def test_field_values_with_nan():
    spec = [holler.Field(int, 10), holler.Field(float, 10), holler.Field(str, 10)]
    result = _get_field_value(spec, [1, float("nan"), "hello"])
    assert result == "         1          hello     "
