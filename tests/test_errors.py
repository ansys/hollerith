import hollerith as holler
import pytest


def test_no_write():
    with pytest.raises(AttributeError):
        holler.write_int(11, 11, 11)


def test_write_not_callable():
    class K:
        write = 1

    with pytest.raises(SystemError):
        holler.write_int(K(), 11, 11)


def test_write_callable_incorrect_args():
    class K:
        def write(self):
            pass

    with pytest.raises(SystemError):
        holler.write_int(K(), 11, 11)
