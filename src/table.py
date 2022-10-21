import typing

import hollerith
import pandas as pd


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
