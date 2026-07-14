import pytest

from quality import data_quality


class FakeCursor:
    def __init__(self, counts):
        self.counts = iter(counts)
        self.queries = []

    def execute(self, query):
        self.queries.append(query)

    def fetchone(self):
        return (next(self.counts),)


class FakeDatabase:
    def __init__(self, counts):
        self.cursor = FakeCursor(counts)
        self.closed = False

    def close(self):
        self.closed = True


def test_run_quality_check_uses_one_connection(monkeypatch):
    database = FakeDatabase([10, 0])
    factory_calls = []

    def database_factory():
        factory_calls.append(True)
        return database

    monkeypatch.setattr(data_quality, "PostgreSQL", database_factory)
    monkeypatch.setattr(data_quality, "TABLES_TO_CHECK", ("raw.fact_orders",))
    monkeypatch.setattr(
        data_quality,
        "QUALITY_RULES",
        (("orders are valid", "SELECT 0"),),
    )

    data_quality.run_quality_check()

    assert len(factory_calls) == 1
    assert len(database.cursor.queries) == 2
    assert database.closed is True


def test_run_quality_check_closes_connection_after_failure(monkeypatch):
    database = FakeDatabase([0])
    monkeypatch.setattr(data_quality, "PostgreSQL", lambda: database)
    monkeypatch.setattr(data_quality, "TABLES_TO_CHECK", ("raw.fact_orders",))
    monkeypatch.setattr(data_quality, "QUALITY_RULES", ())

    with pytest.raises(data_quality.QualityCheckError, match="is empty"):
        data_quality.run_quality_check()

    assert database.closed is True


@pytest.mark.parametrize("relation", ("orders", "raw.", ".orders", "a.b.c"))
def test_relation_identifier_requires_schema_and_table(relation):
    with pytest.raises(ValueError, match="schema.table"):
        data_quality.relation_identifier(relation)
