import io
import typing

import hollerith as holler
import pandas as pd


def _write_table(value: pd.DataFrame, spec: typing.List[holler.Field], numrows: int) -> str:
    s = io.StringIO()
    holler.write_table(s, value, numrows, spec)
    return s.getvalue()


def test_table_1():
    spec = [holler.Field(float, 20), holler.Field(float, 20)]
    value = pd.DataFrame({"a": [1.0, 3.0, 5.0], "b": [2.0, 4.0, 6.0]})
    result = _write_table(value, spec, 3)
    assert (
        result
        == """                 1.0                 2.0
                 3.0                 4.0
                 5.0                 6.0"""
    )


def test_table_2():
    """test table with empty columns"""
    spec = [
        holler.Field(int, 8),
        holler.Field(float, 16),
        holler.Field(float, 16),
        holler.Field(float, 16),
        holler.Field(int, 8),
        holler.Field(int, 8),
    ]
    value = pd.DataFrame(
        {
            "a": [100, 101, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
            "b": [
                -0.2969848,
                -0.2687006,
                -0.160727,
                -0.1454197,
                -0.2969848,
                -0.2687006,
                -0.1454197,
                -0.160727,
                -0.2969848,
                -0.2687006,
                -0.1454197,
                -0.160727,
            ],
            "c": [
                0.2969848,
                0.2687006,
                0.3880294,
                0.3510742,
                0.2969848,
                0.2687006,
                0.3510742,
                0.3880294,
                0.2969848,
                0.2687006,
                0.3510742,
                0.3880294,
            ],
            "d": [0.0, 0.0, 0.0, 0.0, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5],
            "e": [pd.NA] * 12,
            "f": [pd.NA] * 12,
        }
    )
    result = _write_table(value, spec, 12)
    assert (
        result
        == """     100      -0.2969848       0.2969848             0.0                
     101      -0.2687006       0.2687006             0.0                
     104       -0.160727       0.3880294             0.0                
     105      -0.1454197       0.3510742             0.0                
     106      -0.2969848       0.2969848            0.25                
     107      -0.2687006       0.2687006            0.25                
     108      -0.1454197       0.3510742            0.25                
     109       -0.160727       0.3880294            0.25                
     110      -0.2969848       0.2969848             0.5                
     111      -0.2687006       0.2687006             0.5                
     112      -0.1454197       0.3510742             0.5                
     113       -0.160727       0.3880294             0.5                """
    )


def test_table_3():
    spec = [
        holler.Field(int, 8),
        holler.Field(float, 16),
        holler.Field(float, 16),
        holler.Field(float, 16),
        holler.Field(int, 8),
        holler.Field(int, 8),
    ]
    value = pd.DataFrame(
        {
            "a": [2000000, 2000001, 2000002],
            "b": [float("nan"), -2772.1652832, -3093.8891602],
            "c": [float("nan"), 643.8095703, 685.0078125],
            "d": [float("nan"), 376.7990417, 811.2246704],
            "e": [pd.NA, pd.NA, 1],
            "f": [pd.NA, pd.NA, 5],
        }
    )
    result = _write_table(value, spec, 3)
    assert (
        result
        == """ 2000000                                                                
 2000001   -2772.1652832     643.8095703     376.7990417                
 2000002   -3093.8891602     685.0078125     811.2246704       1       5"""
    )


def test_table_4():
    spec = [
        holler.Field(int, width=8),
        holler.Field(float, width=16),
        holler.Field(float, width=16),
        holler.Field(float, width=16),
        holler.Field(int, width=8),
        holler.Field(int, width=8),
    ]

    value = pd.DataFrame(
        {"nid": [69000001], "x": [0.0], "y": [1.0], "z": [1.0], "tc": [1], "rc": [1]}
    )
    result = _write_table(value, spec, 1)
    assert result == "69000001             0.0             1.0             1.0       1       1"
