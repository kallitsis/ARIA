# conftest.py

# conftest.py

import pytest
import brightway2 as bw

@pytest.fixture
def mock_bw(monkeypatch):
    """
    A pytest fixture that monkeypatches brightway2 so that:
      1) Database calls return a mock database with a single matching activity
      2) LCA calls return a fixed 'score' of 42
      3) The mock activity is hashable, so you can do {activity: 1} for functional_unit
    """

    # 1) Mock the LCA class
    class MockLCA:
        def __init__(self, fu, method):
            pass
        def lci(self):
            pass
        def lcia(self):
            self.score = 42  # fixed score for testing

    monkeypatch.setattr(bw, "LCA", MockLCA)

    # 2) Create a hashable MockActivity class
    class MockActivity:
        """
        A mock representing a Brightway2 Activity. 
        Internally stores data in a dict, but is itself hashable.
        """
        def __init__(self, data):
            # data is a dictionary like {"name": "...", "location": "..."}
            self._data = data

        def __getitem__(self, key):
            return self._data[key]

        def __hash__(self):
            # Return a stable hash based on unique fields (e.g., name & location)
            return hash((self._data.get("name"), self._data.get("location")))

        def __eq__(self, other):
            # Two MockActivity are equal if they have the same data
            if not isinstance(other, MockActivity):
                return False
            return self._data == other._data

        def __repr__(self):
            # A human-readable string for debug prints
            return f"MockActivity({self._data})"

    # 3) Mock the Database class
    class MockDatabase:
        def __init__(self, name):
            self.name = name
        def __iter__(self):
            # Return exactly one activity that matches "dummy process" & "GLO"
            yield MockActivity({"name": "dummy process", "location": "GLO"})

    monkeypatch.setattr(bw, "Database", MockDatabase)

    # 4) Also ensure 'databases' has our ecoinvent key
    monkeypatch.setattr(bw, "databases", {"ecoinvent-3.10.1-cutoff": "mocked"})

    return bw

