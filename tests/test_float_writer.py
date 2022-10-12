import io

import hollerith as holler
import pytest


def _write_float(value: float, width: int) -> str:
    s = io.StringIO()
    holler.write_float(s, value, width)
    return s.getvalue()


# same as tests for _write_float - but for revised version: _write_float2
def test_write_float_001():
    assert _write_float(1.0, 10) == "       1.0"


def test_write_float_002():
    """Test values from issue #75."""
    assert _write_float(-52.19347754803565, 16) == "-52.193477548036"
    assert _write_float(93.07127275523395, 16) == " 93.071272755234"
    assert _write_float(132.15396553437066, 16) == " 132.15396553437"


def test_write_float_003():
    assert _write_float(-1.9510575969873e-05, 16) == "-1.951057597e-05"


def test_write_float_004():
    """Test small and large values for narrow fields

    Note
    ----
    Formatter scheme for specifier `g`:
    - scientific: (-1e-4, +1e-4)
    - scientific: [1e6, inf)
    - scientific: (-inf, -1e6]
    - fixed: (-1e6, -1e-4]
    - fixed: [1e-4, 1e6)
    """
    # scientific format
    assert _write_float(-0.00000321893890, 10) == "-3.219e-06"
    assert _write_float(+0.00000321893890, 10) == "3.2189e-06"
    assert _write_float(+0.00000321896890, 10) == " 3.219e-06"  # edge case (rounding)
    assert _write_float(+0.00000321876890, 10) == "3.2188e-06"
    assert _write_float(-0.00000321876890, 10) == "-3.219e-06"
    assert _write_float(-321876896312513.0, 10) == "-3.219e+14"
    # fixed format
    assert _write_float(133.1235342, 10) == " 133.12353"
    assert _write_float(+0.001351235342, 10) == "0.00135124"
    assert _write_float(-0.001351254342, 10) == "-0.0013513"  # rounding
    assert _write_float(-0.0001351235342, 10) == "-0.0001351"


@pytest.mark.parametrize("width", [10, 16, 20])
@pytest.mark.parametrize("exponent", range(-24, 24, 1))
@pytest.mark.parametrize("value", [-1.5184023950181023415, 1.51840239501])
def test_write_float_005(width, exponent, value):
    """Test formatted length of list of numbers."""
    number = value * (10**exponent)
    assert len(_write_float(number, width)) == width


def test_write_float_006():
    """Test large integer-like floats."""
    assert _write_float(float(12345678), 10) == "12345678.0"
    assert _write_float(float(1234567891234), 10) == "1.2346e+12"
    assert _write_float(float(-1234567891234), 10) == "-1.235e+12"
    assert _write_float(float(1234567891234), 16) == " 1234567891234.0"
    assert _write_float(float(-1234567891234), 16) == "-1234567891234.0"


def test_write_float_007():
    """Edge case for formatting integer-like floats.

    Note
    ----
    Format as scientific?

    """
    assert _write_float(float(-12345678), 10) == " -12345678"
