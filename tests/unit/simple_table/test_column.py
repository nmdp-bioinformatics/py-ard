from pyard.simple_table import Column


def test_column_creation():
    col = Column("age", ["25", "30", "35"])
    assert col.name == "-age"
    assert len(col) == 3


def test_column_apply():
    col = Column("age", ["25", "30"])
    result = col.apply(lambda x: int(x) * 2)
    assert result == [50, 60]


def test_column_to_list():
    col = Column("name", ["John", "Jane"])
    assert col.to_list() == ["John", "Jane"]


def test_column_getitem():
    col = Column("age", ["25", "30", "35"])
    assert col[0] == "25"
    assert col[1] == "30"
    assert col[-1] == "35"


def test_column_iter():
    col = Column("name", ["John", "Jane"])
    values = list(col)
    assert values == ["John", "Jane"]


def test_column_len():
    col = Column("empty", [])
    assert len(col) == 0

    col = Column("data", ["a", "b", "c"])
    assert len(col) == 3


def test_column_name_property():
    col = Column("test_column", ["value"])
    assert col.name == "-test_column"
