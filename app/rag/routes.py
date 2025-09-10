# ============================================================================
# REST Client Setup
# ============================================================================
from fastapi import APIRouter, Depends
import weaviate
from langchain_openai import OpenAIEmbeddings
import json
import logging
import httpx
from typing import Dict
import datetime
from dotenv import load_dotenv

from .model.models import RagRequest, RagResponse, HealthStatus, ServiceStatus
from .tools.rag_chain import RagChain
from .tools.rag_worker import RagWorker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
REQUEST_TIMEOUT = 30.0

router = APIRouter(prefix="/rag", tags=["rag"])

class RagMgr:
    
    def __init__(self):
        self.timeout = httpx.Timeout(REQUEST_TIMEOUT)
        load_dotenv() 
        logger.info("Fetching embedding")
        self.embeddings = OpenAIEmbeddings()
        self.weaviate_client = weaviate.connect_to_local(port=8080)
        logger.info("Setting up RagChain")
        self.rag_worker = RagWorker(self.weaviate_client, self.embeddings)
        self.rag_chain = RagChain(self.rag_worker)
        logger.info("RestClient initialized")

ragMgr = RagMgr()


@router.get("/healthCheck", response_model=HealthStatus)
def health_check():
    hstatus = HealthStatus()
    hstatus.timestamp = datetime.now()
    if restClient.embeddings is None or restClient.weaviate_client is None:
        hstatus.status = ServiceStatus.ONLINE
    else: 
        hstatus.status = ServiceStatus.OFFLINE
    return hstatus    

@router.post('/askrag', response_model=RagResponse)
async def post(self, request: RagRequest) -> Dict:
    """
    API endpoint to process question.
    Expects a JSON payload with a 'question' key.
    """
    json_string = request.model_dump_json()
    data = json.loads(json_string)
    if not data or 'question' not in data:
        return json.dumps({'error': 'Missing "question" in request body'}), 400

    question = data['question']
    context = data['context']
    logger.info("Processing question")

    answer = ragMgr.rag_chain.invoke(question, context)
    response = RagResponse(question=question, context=context, answer=answer)

    logger.info(response)

    return response
