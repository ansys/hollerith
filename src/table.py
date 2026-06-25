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

import typing

import pandas as pd

import hollerith


def write_table(buffer, table: pd.DataFrame, numrows: int, spec: typing.List[hollerith.Field]):
    """Write table to buffer with fixed width columns

    Parameters
    ----------
    buffer :
        Buffer to write to - it could be a file or a StringIO object, for example. The only
        requirement is that it must contain a write attribute that is callable with a single
        string argument.
    table : pandas.DataFrame
        Table to write.
    numrows : int
        The number of rows to write. This might be larger than the length of `table`.
        If so, append with empty lines with the right size.
    spec : List[hollerith.Field]
        Specification of the table. Must be the same length as the number of columns in `table`.

    Notes
    -----
    Here, we convert the table to a numpy 2-d array with a type of object in order to call
    :class:`write_numpy_table <hollerith._writer.write_numpy_table>`.
    Numpy arrays of a narrower type are possible, such
    as arrays of ints or floats, and this conversion can be expensive. A future optimization
    would be to expose Cython-level methods in `_writer`.

    Examples
    --------
    >>> import io
    >>> import hollerith as holler
    >>> import pandas as pd
    >>> buffer = io.StringIO()
    >>> spec = [holler.Field(float, 20), holler.Field(float, 20)]
    >>> table = pd.DataFrame({"a": [1.0, 3.0, 5.0], "b": [2.0, 4.0, 6.0]})
    >>> result = holler.write_table(buffer, table, 3, spec)
    >>> print(buffer.getvalue())
        '             1.0                 2.0
                      3.0                 4.0
                      5.0                 6.0'
    """
    numpy_table = table.to_numpy().astype(object)
    hollerith._writer.write_numpy_table(buffer, spec, numrows, numpy_table)
