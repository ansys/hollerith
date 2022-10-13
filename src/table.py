import typing

import hollerith
import pandas as pd


def write_table(buffer, table: pd.DataFrame, numrows: int, spec: typing.List[hollerith.Field]):
    """
    Write table to buffer with fixed width columns

    buffer:
        Buffer to write to - it could be a file or a StringIO object, for example. The only
        requirement is that itt must contain a write attribute that is callable with a single
        string argument.
    table: pandas.DataFrame
        Table to write, represented as a pandas DataFrame.
    spec: list
        Specification of the table. Must be the same length as the number of columns in `table`.
    numrows: int
        The number of rows to write. This might be larger than the length of `table`.
        If so, append with empty lines with the right size.
    """
    # write_numpy_table expects a numpy array of object.  tables of a narrower type are possible,
    # such as int or float, but to avoid specializing write_numpy_table, we cast to object here.
    # a future optimization could be to avoid this and write multiple table kinds.
    numpy_table = table.to_numpy().astype(object)
    hollerith._writer.write_numpy_table(buffer, spec, numrows, numpy_table)
