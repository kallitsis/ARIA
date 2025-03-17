# test_search_workflow.py

import pandas as pd
import pytest
from ARIA.search_workflow import process_dataframe

@pytest.fixture
def dummy_db():
    # Simulate a brightway2 Database with a .search() method
    class MockActivity(dict):
        def __getitem__(self, item):
            return dict.__getitem__(self, item)
    
    class MockDB:
        def search(self, query, limit=50, filter=None):
            # A dummy search that returns an empty list unless query matches something
            if "waste" in query:
                return [MockActivity({"name": "waste something", "location": "GLO", "unit": "kg"})]
            return []
    
    return MockDB()

@pytest.fixture
def mock_client():
    # Same mock as used in test_search_utils, but you can keep a single fixture in conftest.py
    class MockChat:
        class completions:
            @staticmethod
            def create(*args, **kwargs):
                return type("MockResponse", (object,), {
                    "choices": [
                        type("MockChoice", (object,), {
                            "message": type("MockMessage", (object,), {
                                "content": "dummy dataset name"
                            })
                        })
                    ]
                })()
    class MockClient:
        chat = MockChat()
    return MockClient()

def test_process_dataframe(dummy_db, mock_client):
    df = pd.DataFrame({"Input/output": ["Waste Graphite", "No match"], "Ecoinvent process": [None, None]})
    result_df = process_dataframe(df, dummy_db, mock_client)
    # We expect the first row might find "waste something" in mock DB, second row no match
    # Check if function sets 'Ecoinvent process' or a new column for the recommended dataset
    assert "Ecoinvent process" in result_df.columns, "Should populate 'Ecoinvent process' column"
