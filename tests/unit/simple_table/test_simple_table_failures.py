import pytest
import csv
import io
from pyard.simple_table import Table


def test_to_dict_same_columns_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError, match="must be different"):
        table.to_dict("name", "name")
    table.close()


def test_to_dict_invalid_columns_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError, match="must be in the table"):
        table.to_dict("invalid", "age")
    table.close()


def test_union_different_columns_fails():
    table1 = Table([("John", "25")], ["name", "age"])
    table2 = Table([("NYC",)], ["city"])
    with pytest.raises(ValueError, match="same columns"):
        table1.union(table2)
    table1.close()
    table2.close()


def test_group_by_invalid_column_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError):
        table.group_by("invalid_column")
    table.close()


def test_getitem_invalid_column_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError):
        table["invalid_column"]
    table.close()


def test_where_invalid_syntax_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError):
        table.where("invalid syntax >>>")
    table.close()


def test_explode_invalid_column_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError):
        table.explode("invalid_column", ";")
    table.close()


def test_value_counts_invalid_column_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError):
        table.value_counts("invalid_column")
    table.close()


def test_rename_invalid_column_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError):
        table.rename({"invalid_column": "new_name"})
    table.close()


def test_concat_columns_invalid_column_fails():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    table = Table(reader, ["name", "age"])
    with pytest.raises(ValueError):
        table.concat_columns(["name", "invalid_column"])
    table.close()


def test_invalid_query():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]

    table = Table(reader, columns)
    with pytest.raises(Exception):
        table.query("SELECT * FROM non_existent_table")
    table.close()
