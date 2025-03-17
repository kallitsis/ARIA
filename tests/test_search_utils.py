# test_search_utils.py

import pytest
from ARIA.search_utils import build_search_query, get_alternative_search_terms

@pytest.fixture
def mock_client():
    # A mock or minimal object that simulates an openai-like API client
    # For now, let's just create a dummy class with a chat attribute
    class MockChat:
        class completions:
            @staticmethod
            def create(*args, **kwargs):
                # Return a dummy response that looks like the real chat completion
                return type("MockResponse", (object,), {
                    "choices": [
                        type("MockChoice", (object,), {
                            "message": type("MockMessage", (object,), {
                                "content": "alternative one, alternative two, alternative three"
                            })
                        })
                    ]
                })()
                
    class MockClient:
        chat = MockChat()
    return MockClient()

def test_build_search_query():
    query = build_search_query("waste graphite")
    assert query == "*waste* *graphite*", "Query was not correctly formatted."

def test_get_alternative_search_terms(mock_client):
    suggestions = get_alternative_search_terms(mock_client, "waste graphite")
    assert len(suggestions) == 3
    assert suggestions == ["alternative one", "alternative two", "alternative three"]
