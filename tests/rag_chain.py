import pytest
from unittest.mock import Mock

from app import RagWorker, RagChain


class RagChain:

    def __init__(self, ):
            self.embeddings = Mock()
            self.weaviate_client = Mock()
 
@pytest.fixture
def rag_chain():
    return RagChain()

def test_rag_chain_invoke(self, rag_chain):

    try:

        rag_worker = RagWorker(rag_chain.weaviate_client, rag_chain.embeddings)
        rag_chain = RagChain(rag_worker)

        query = "What did the president say about George Washington"
        context = "2025 - State of the Union"
        output = rag_chain.invoke(query,context)
        print(output)
        assert output is not None

    except Exception as e:
        print(f"An error occurred during the request: {e}")
    finally:
        self.weaviate_client.close()
