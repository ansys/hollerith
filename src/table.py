import typing
import hollerith

import pandas as pd


def write_table(buffer, table: pd.DataFrame, numrows: int, spec: typing.List[hollerith.Field]):
    """
    buffer: buffer to write to - it could be a file or a StringIO object, for example
    spec: specification of the table.
    numrows: int
        the number of rows to write. This might be larger than the size of the numpy
        array suggests, if so, append with empty lines with the right size.
    arr: 2d numpy array of the table data

    assume by now that all empty columns are already added to the spec
    """
    # write_numpy_table expects a numpy array of object.  tables of a narrower type are possible,
    # such as int or float, but to avoid specializing write_numpy_table, we cast to object here.
    # a future optimization could be to avoid this and write multiple table kinds.
    numpy_table = table.to_numpy().astype(object)
    hollerith._writer.write_numpy_table(buffer, spec, numrows, numpy_table)
