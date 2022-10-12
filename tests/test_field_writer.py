import io
import typing

import hollerith as holler


def write_field(
    buf: typing.IO[typing.AnyStr], field_type: type, value: typing.Any, width: int
) -> None:
    if field_type == None:
        holler.write_spaces(buf, width)
    elif field_type == str:
        holler.write_string(buf, value, width)
    elif field_type == int:
        holler.write_int(buf, value, width)
    elif field_type == float:
        holler.write_float(buf, value, width)


def _get_field_value(fields: typing.List[holler.Field], values: typing.List) -> str:
    s = io.StringIO()
    [write_field(s, field.type, value, field.width) for field, value in zip(fields, values)]
    return s.getvalue()


def test_field_values_int_string():
    """test integer and string field values"""
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
