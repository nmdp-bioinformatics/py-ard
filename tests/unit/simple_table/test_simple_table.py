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


def test_table_from_tuples():
    data = [("John", "25"), ("Jane", "30")]
    columns = ["name", "age"]
    table = Table(data, columns)
    result = table.query("SELECT * FROM data")
    assert len(result) == 2
    assert result[0] == ("John", "25")
    table.close()


def test_columns_property():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    assert table.columns == ["name", "age"]
    table.close()


def test_head():
    csv_data = "name,age\nJohn,25\nJane,30\nBob,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    head_result = table.head(2)
    assert len(head_result.rows) == 2
    table.close()


def test_tail():
    csv_data = "name,age\nJohn,25\nJane,30\nBob,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    tail_result = table.tail(2)
    assert len(tail_result.rows) == 2
    table.close()


def test_group_by():
    csv_data = "city,age\nNYC,25\nLA,30\nNYC,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["city", "age"]
    table = Table(reader, columns)
    grouped = table.group_by("city")
    assert "NYC" in grouped
    assert len(grouped["NYC"]) == 2
    table.close()


def test_unique_single_column():
    csv_data = "city,age\nNYC,25\nLA,30\nNYC,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["city", "age"]
    table = Table(reader, columns)
    unique_cities = table.unique("city")
    assert len(unique_cities) == 2
    table.close()


def test_unique_multiple_columns():
    csv_data = "city,age\nNYC,25\nLA,30\nNYC,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["city", "age"]
    table = Table(reader, columns)
    unique_table = table.unique(["city", "age"])
    assert len(unique_table) == 2
    unique_table.close()
    table.close()


def test_where():
    csv_data = "name,age\nJohn,25\nJane,30"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    filtered = table.where("age > 25")
    assert len(filtered) == 1
    filtered.close()
    table.close()


def test_where_not_null():
    data = [("John", "25"), ("Jane", None), ("Bob", "35")]
    columns = ["name", "age"]
    table = Table(data, columns)
    filtered = table.where_not_null("age")
    assert len(filtered) == 2
    filtered.close()
    table.close()


def test_where_in():
    csv_data = "name,age\nJohn,25\nJane,30\nBob,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    filtered = table.where_in("name", {"John", "Jane"}, ["name", "age"])
    assert len(filtered) == 2
    filtered.close()
    table.close()


def test_to_dict():
    csv_data = "name,age\nJohn,25\nJane,30"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    result_dict = table.to_dict("name", "age")
    assert result_dict["John"] == "25"
    assert result_dict["Jane"] == "30"
    table.close()


def test_value_counts():
    csv_data = "city,age\nNYC,25\nLA,30\nNYC,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["city", "age"]
    table = Table(reader, columns)
    counts = table.value_counts("city")
    result = counts.query("SELECT * FROM data_counts")
    assert len(result) == 2
    counts.close()
    table.close()


def test_agg():
    csv_data = "city,age\nNYC,25\nLA,30\nNYC,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["city", "age"]
    table = Table(reader, columns)
    result = table.agg("city", "age", list)
    assert "NYC" in result
    table.close()


def test_getitem_multiple_columns():
    csv_data = "name,age,city\nJohn,25,NYC\nJane,30,LA"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age", "city"]
    table = Table(reader, columns)
    subset = table[["name", "city"]]
    assert len(subset) == 2
    subset.close()
    table.close()


def test_rename():
    csv_data = "name,age\nJohn,25"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    table.rename({"name": "full_name"})
    assert "full_name" in table.columns
    table.close()


def test_union():
    data1 = [("John", "25")]
    data2 = [("Jane", "30")]
    columns = ["name", "age"]
    table1 = Table(data1, columns)
    table2 = Table(data2, columns)
    union_table = table1.union(table2)
    assert len(union_table) == 2
    union_table.close()
    table1.close()
    table2.close()


def test_remove():
    csv_data = "name,age\nJohn,25\nJane,30\nBob,35"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    table.remove("name", ["John"])
    assert len(table) == 2
    table.close()


def test_concat_columns():
    csv_data = "first,last\nJohn,Doe\nJane,Smith"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["first", "last"]
    table = Table(reader, columns)
    concat_col = table.concat_columns(["first", "last"])
    assert concat_col[0] == "JohnDoe"
    table.close()


def test_explode():
    csv_data = "name,tags\nJohn,a;b\nJane,c"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "tags"]
    table = Table(reader, columns)
    exploded = table.explode("tags", ";")
    assert len(exploded) == 3
    exploded.close()
    table.close()


def test_len():
    csv_data = "name,age\nJohn,25\nJane,30"
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = ["name", "age"]
    table = Table(reader, columns)
    assert len(table) == 2
    table.close()
