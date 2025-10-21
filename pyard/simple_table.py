import sqlite3
import csv
import itertools
from collections import defaultdict
from typing import List


class Table:
    def __init__(self, data, columns: list, table_name: str = "data"):
        self._conn = sqlite3.connect(":memory:")
        self._name = table_name
        self._columns = columns
        if isinstance(data, csv.DictReader):
            self._create_table_from_reader(data, columns)
        else:
            self._create_table_from_tuples(data, columns)

    def _create_table_from_reader(self, reader: csv.DictReader, columns: list):
        rows = list(reader)
        if not rows:
            return

        column_defs = ", ".join(f"`{col}` TEXT" for col in columns)

        self._conn.execute(f"CREATE TABLE {self._name} ({column_defs})")

        placeholders = ", ".join("?" * len(columns))
        for row in rows:
            values = [row[col] for col in columns]
            self._conn.execute(
                f"INSERT INTO {self._name} VALUES ({placeholders})", values
            )

        self._conn.commit()

    def _create_table_from_tuples(self, data: list, columns: list):
        if not data:
            return

        column_defs = ", ".join(f"`{col}` TEXT" for col in columns)

        self._conn.execute(f"CREATE TABLE {self._name} ({column_defs})")

        placeholders = ", ".join("?" * len(columns))
        for row in data:
            self._conn.execute(f"INSERT INTO {self._name} VALUES ({placeholders})", row)

        self._conn.commit()

    def query(self, sql: str):
        return self._conn.execute(sql).fetchall()

    def close(self):
        if hasattr(self, "_conn") and self._conn:
            self._conn.close()

    @property
    def columns(self):
        cursor = self._conn.execute(f"PRAGMA table_info({self._name})")
        return [row[1] for row in cursor.fetchall()]

    def head(self, n: int = 5):
        cursor = self._conn.execute(f"SELECT * FROM {self._name} LIMIT {n}")
        rows = cursor.fetchall()
        return PrintableTable(self.columns, rows)

    def tail(self, n: int = 5):
        cursor = self._conn.execute(
            f"SELECT * FROM {self._name} ORDER BY rowid DESC LIMIT {n}"
        )
        rows = cursor.fetchall()
        return PrintableTable(self.columns, rows)

    def group_by(self, group_by_column: str, return_columns: List[str] = None):
        if group_by_column not in self.columns:
            raise ValueError(f"Column '{group_by_column}' not found in table")
        if return_columns is None:
            return_columns = self.columns
        column_names = ", ".join([f"`{col}`" for col in return_columns])
        cursor = self._conn.execute(
            f"SELECT {column_names} FROM {self._name} ORDER BY `{group_by_column}`"
        )
        rows = cursor.fetchall()
        col_index = self.columns.index(group_by_column)
        grouped = itertools.groupby(rows, key=lambda row: row[col_index])
        return {
            key: [{col: row[i] for i, col in enumerate(self.columns)} for row in group]
            for key, group in grouped
        }

    def unique(self, columns):
        if isinstance(columns, str):
            cursor = self._conn.execute(
                f"SELECT DISTINCT `{columns}` FROM {self._name}"
            )
            values = [row[0] for row in cursor.fetchall()]
            return Column(columns, values)
        else:
            column_names = ", ".join([f"`{col}`" for col in columns])
            cursor = self._conn.execute(
                f"SELECT DISTINCT {column_names} FROM {self._name}"
            )
            return Table(cursor.fetchall(), columns, f"{self._name}_unique")

    def where(self, where_clause: str):
        try:
            cursor = self._conn.execute(
                f"SELECT * FROM {self._name} WHERE {where_clause}"
            )
            return Table(cursor.fetchall(), self.columns, f"{self._name}_filtered")
        except Exception as e:
            raise ValueError(f"Invalid WHERE clause: {where_clause}") from e

    def where_not_null(self, null_column):
        if isinstance(null_column, list):
            conditions = " AND ".join([f"`{col}` IS NOT NULL" for col in null_column])
            table_suffix = "_".join(null_column)
        else:
            conditions = f"`{null_column}` IS NOT NULL"
            table_suffix = null_column

        table_name = f"{self._name}_not_null_{table_suffix}"
        cursor = self._conn.execute(f"SELECT * FROM {self._name} WHERE {conditions}")
        return Table(cursor.fetchall(), table_name=table_name, columns=self.columns)

    def where_in(self, column_name: str, values: set, columns: list):
        placeholders = ", ".join("?" * len(values))
        column_names = ", ".join([f"`{col}`" for col in columns])
        cursor = self._conn.execute(
            f"SELECT {column_names} FROM {self._name} WHERE `{column_name}` IN ({placeholders})",
            list(values),
        )
        return Table(cursor.fetchall(), columns, f"{self._name}_filtered")

    def to_dict(self, key_column: str = None, value_column: str = None):
        if not key_column and not value_column:
            key_column, value_column = self.columns
        elif key_column not in self.columns or value_column not in self.columns:
            raise ValueError(
                f"Columns {key_column} and {value_column} must be in the table"
            )
        if key_column == value_column:
            raise ValueError(
                f"Columns {key_column} and {value_column} must be different"
            )
        cursor = self._conn.execute(
            f"SELECT `{key_column}`, `{value_column}` FROM {self._name}"
        )
        return dict(cursor.fetchall())

    def value_counts(self, column: str):
        if column not in self.columns:
            raise ValueError(f"Column '{column}' not found in table")
        cursor = self._conn.execute(
            f"SELECT `{column}`, COUNT(*) FROM {self._name} GROUP BY `{column}` ORDER BY COUNT(*) DESC"
        )
        return Table(cursor.fetchall(), [column, "count"], f"{self._name}_counts")

    def agg(self, group_column: str, agg_column: str, func):
        builtin_funcs = {list, set}
        query = f"SELECT `{group_column}`, `{agg_column}` FROM {self._name} GROUP BY `{group_column}`, `{agg_column}`"
        result = self._conn.execute(query).fetchall()
        d = defaultdict(list)
        for k, v in result:
            d[k].append(v)
        for k, v in d.items():
            d[k] = func(v)
        if func in builtin_funcs:
            return d
        return Table(list(d.items()), [group_column, "agg"], f"{self._name}_agg")

    def __setitem__(self, column: str, values):
        if column in self.columns:
            self._conn.execute(f"ALTER TABLE {self._name} DROP COLUMN `{column}`")
        self._conn.execute(f"ALTER TABLE {self._name} ADD COLUMN `{column}` TEXT")
        for i, value in enumerate(values):
            self._conn.execute(
                f"UPDATE {self._name} SET `{column}` = ? WHERE rowid = ?",
                (value, i + 1),
            )
        self._conn.commit()

    def __getitem__(self, column):
        if isinstance(column, list):
            for col in column:
                if col not in self.columns:
                    raise ValueError(f"Column '{col}' not found in table")
            column_names = ", ".join([f"`{col}`" for col in column])
            result = self._conn.execute(
                f"SELECT {column_names} FROM {self._name}"
            ).fetchall()
            return Table(result, column, f"{self._name}_subset")
        else:
            if column not in self.columns:
                raise ValueError(f"Column '{column}' not found in table")
            result = self._conn.execute(
                f"SELECT `{column}` FROM {self._name}"
            ).fetchall()
            values = [row[0] for row in result]
            return Column(column, values)

    def rename(self, column_mapping: dict):
        for old_name, new_name in column_mapping.items():
            if old_name not in self.columns:
                raise ValueError(f"Column '{old_name}' not found in table")
            self._conn.execute(
                f"ALTER TABLE {self._name} RENAME COLUMN `{old_name}` TO `{new_name}`"
            )
        self._conn.commit()
        return self

    def union(self, other_table):
        if self.columns != other_table.columns:
            raise ValueError("Tables must have the same columns for union")

        self_data = self._conn.execute(f"SELECT * FROM {self._name}").fetchall()
        other_data = other_table._conn.execute(
            f"SELECT * FROM {other_table._name}"
        ).fetchall()

        union_data = self_data + other_data
        return Table(union_data, self.columns, f"{self._name}_union")

    def remove(self, column_name: str, values):
        placeholders = ", ".join("?" * len(values))
        self._conn.execute(
            f"DELETE FROM {self._name} WHERE `{column_name}` IN ({placeholders})",
            list(values),
        )
        self._conn.commit()
        return self

    def concat_columns(self, columns: list):
        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column '{col}' not found in table")
        column_names = " || ".join([f"`{col}`" for col in columns])
        result = self._conn.execute(
            f"SELECT {column_names} FROM {self._name}"
        ).fetchall()
        values = [row[0] for row in result]
        concat_name = "_".join(columns)
        return Column(concat_name, values)

    def explode(self, column: str, delimiter: str):
        if column not in self.columns:
            raise ValueError(f"Column '{column}' not found in table")
        all_data = self._conn.execute(f"SELECT * FROM {self._name}").fetchall()
        col_index = self.columns.index(column)

        exploded_data = []
        for row in all_data:
            if row[col_index]:
                split_values = row[col_index].split(delimiter)
                for value in split_values:
                    new_row = list(row)
                    new_row[col_index] = value.strip()
                    exploded_data.append(tuple(new_row))
            else:
                exploded_data.append(row)

        return Table(exploded_data, self.columns, f"{self._name}_exploded")

    def __len__(self):
        cursor = self._conn.execute(f"SELECT COUNT(*) FROM {self._name}")
        return cursor.fetchone()[0]

    def __str__(self):
        return str(self.head()) + "\n" + "." * 10 + "\n" + str(self.tail())

    def __repr__(self):
        return str(self)

    def __del__(self):
        self.close()


class Column:
    def __init__(self, name, values):
        self._name = name
        self._values = values

    @property
    def name(self):
        return f"-{self._name}"

    def apply(self, func):
        return [func(value) for value in self._values]

    def to_list(self):
        return list(self._values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        return self._values[index]

    def __iter__(self):
        return iter(self._values)


class PrintableTable:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    def __str__(self):
        if not self.rows:
            return ""

        # Calculate column widths
        widths = [len(col) for col in self.columns]
        for row in self.rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        # Create header
        header = (
            "| "
            + " | ".join(col.ljust(widths[i]) for i, col in enumerate(self.columns))
            + " |"
        )
        separator = "|" + "".join("-" * (w + 2) + "|" for w in widths)

        # Create rows
        result = [separator, header, separator]
        for row in self.rows:
            row_str = (
                "| "
                + " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
                + " |"
            )
            result.append(row_str)
        result.append(separator)

        return "\n".join(result)
