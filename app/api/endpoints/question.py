from fastapi import APIRouter,  Body
from pydantic import BaseModel
from app.services.question_process import get_conversation_chain, handle_question
from app.api.endpoints import utils
router = APIRouter()


class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request_body: QuestionRequest = Body(...)):
    question = request_body.question
    try:
        # Retrieve the vector store from the global variable
        if utils.global_vector_store is None:
            return {"error": "No vector store available. Please upload a PDF first."}

        # Get the conversation chain
        conversation_chain = get_conversation_chain(utils.global_vector_store)

        if conversation_chain is None:
            return {"error": "No relevant document found"}

        # Handle the question
        response = handle_question(question, conversation_chain)

        return response
    except Exception as e:
        return {"error": str(e)}



        