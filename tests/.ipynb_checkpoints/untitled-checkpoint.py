# conftest.py

import pytest
import brightway2 as bw

@pytest.fixture
def mock_bw(monkeypatch):
    """
    A pytest fixture that monkeypatches brightway2 so that:
      1) Database calls return a mock database with a single matching activity
      2) LCA calls return a fixed 'score' of 42

    This allows tests to run offline without requiring the real ecoinvent DB.
    """

    # 1) Mock the LCA class
    class MockLCA:
        def __init__(self, fu, method):
            pass
        def lci(self):
            pass
        def lcia(self):
            self.score = 42  # Fixed score for testing

    monkeypatch.setattr(bw, "LCA", MockLCA)

    # 2) Mock the Database class
    class MockActivity(dict):
        pass

    class MockDatabase:
        def __init__(self, name):
            self.name = name

        def __iter__(self):
            # For simplicity, return a single activity that matches 'dummy process' in 'GLO'
            yield MockActivity({"name": "dummy process", "location": "GLO"})

    monkeypatch.setattr(bw, "Database", MockDatabase)

    # 3) Also mock the 'databases' dict so the code sees "ecoinvent-3.10.1-cutoff" as loaded
    monkeypatch.setattr(bw, "databases", {"ecoinvent-3.10.1-cutoff": "mocked"})

    # Return the brightway2 module, if needed in tests
    return bw
