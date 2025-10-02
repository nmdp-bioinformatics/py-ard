import pytest
import csv
import io
from pyard.simple_table import Table


def test_create_table_with_data():
    csv_data = "name,age,city\nJohn,25,NYC\nJane,30,LA"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age", "city"]

    table = Table(reader, columns)
    result = table.query("SELECT * FROM data")

    assert len(result) == 2
    assert result[0] == ("John", "25", "NYC")
    assert result[1] == ("Jane", "30", "LA")
    table.close()


def test_empty_reader():
    reader = csv.DictReader(io.StringIO(""))
    columns = ["name", "age"]

    table = Table(reader, columns)
    result = table.query("SELECT name FROM sqlite_master WHERE type='table'")

    assert len(result) == 0
    table.close()


def test_custom_table_name():
    csv_data = "id,value\n1,test"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["id", "value"]

    table = Table(reader, columns, "custom")
    result = table.query("SELECT * FROM custom")

    assert result[0] == ("1", "test")
    table.close()


def test_invalid_query():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]

    table = Table(reader, columns)
    with pytest.raises(Exception):
        table.query("SELECT * FROM non_existent_table")
    table.close()


def test_query_with_where_clause():
    csv_data = "name,age\nJohn,25\nJane,30"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]

    table = Table(reader, columns)
    result = table.query("SELECT * FROM data WHERE age > 25")

    assert len(result) == 1
    assert result[0] == ("Jane", "30")
    table.close()


def test_query_with_order_by():
    csv_data = "name,age\nJohn,25\nJane,30"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]

    table = Table(reader, columns)
    result = table.query("SELECT * FROM data ORDER BY age DESC")

    assert len(result) == 2
    assert result[0] == ("Jane", "30")
    assert result[1] == ("John", "25")
    table.close()


def test_select_column_with_subscript_operator():
    csv_data = "name,age\nJohn,25\nJane,30"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]

    table = Table(reader, columns)
    ages = table["age"]

    assert len(ages) == 2
    assert ages[0] == "25"
    assert ages[1] == "30"


def test_create_new_column_with_subscript_operator():
    csv_data = "name,age\nJohn,25\nJane,30"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]

    table = Table(reader, columns)
    table["double_age"] = table["age"].apply(lambda x: int(x) * 2)
    double_ages = table["double_age"]

    assert len(double_ages) == 2
    assert double_ages[0] == "50"
    assert double_ages[1] == "60"
