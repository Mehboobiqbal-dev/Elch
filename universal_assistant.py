from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PromptRequest, PromptResponse
from core.db import get_db
from planner import generate_plan
from intent_extractor import extract_intents
from execution_engine import execute_step
from knowledge_base import KnowledgeBase
from tool_manager import ToolManager
from evaluation import evaluate_plan_execution
from gemini import generate_text
import logging
# from self_learning import learn_from_execution

router = APIRouter()

MAX_ITERATIONS = 10

def classify_question_type(question: str) -> str:
    """
    Classify if a question is general knowledge or requires specific tools/browser actions.
    Returns 'general' for general questions, 'task' for tasks requiring tools.
    """
    classification_prompt = f"""
    Classify the following user input as either 'general' or 'task':

    - 'general': Questions about facts, explanations, advice, opinions, or general knowledge that can be answered directly with information
    - 'task': Requests that require performing actions like browsing websites, filling forms, making purchases, interacting with web applications, or any automated task

    Examples:
    - "What is the capital of France?" → general
    - "Explain quantum physics" → general
    - "What's the weather today?" → general
    - "Book a flight to Paris" → task
    - "Search for hotels in London" → task
    - "Fill out this form" → task
    - "Order pizza online" → task

    User input: "{question}"

    Respond with only 'general' or 'task':
    """

    try:
        response = generate_text(classification_prompt).strip().lower()
        if 'general' in response:
            return 'general'
        elif 'task' in response:
            return 'task'
        else:
            # Default to task if classification is unclear
            return 'task'
    except Exception as e:
        logging.warning(f"Question classification failed: {e}, defaulting to task")
        return 'task'

def answer_general_question(question: str, context: str = "") -> str:
    """
    Answer general questions using Gemini API with optional context.
    """
    if context:
        prompt = f"""
        Answer the following question based on the provided context and your general knowledge.
        If the context is relevant, use it to inform your answer. If not, answer based on your general knowledge.

        Context: {context}

        Question: {question}

        Provide a comprehensive but concise answer:
        """
    else:
        prompt = f"""
        Answer the following question based on your general knowledge:

        Question: {question}

        Provide a comprehensive but concise answer:
        """

    try:
        return generate_text(prompt)
    except Exception as e:
        logging.error(f"Failed to generate answer for general question: {e}")
        return "I'm sorry, I encountered an error while trying to answer your question. Please try again."

@router.post("/prompt", response_model=PromptResponse)
def handle_prompt(request: PromptRequest, db: Session = Depends(get_db)):
    tool_manager = ToolManager()
    """Handles a user prompt by generating a plan and executing it with self-correction."""
    try:
        # First, classify if this is a general question or requires tools
        question_type = classify_question_type(request.prompt)

        if question_type == 'general':
            # Handle as general question using Gemini
            logging.info(f"Classified as general question: {request.prompt}")
            kb = KnowledgeBase()
            # Try to get relevant context from knowledge base
            try:
                context_docs = kb.search(request.prompt, k=3)
                context = "\n".join([doc.get('content', '') for doc in context_docs])
            except:
                context = ""

            answer = answer_general_question(request.prompt, context)

            return {
                "status": "success",
                "message": "Answered general question using AI knowledge.",
                "steps": [{"step": {"action": "answer_general_question", "params": {"question": request.prompt}},
                         "result": answer, "error": None}],
                "evaluation_score": 1.0
            }

        # For tasks, proceed with the existing tool-based approach
        kb = KnowledgeBase()
        intents = extract_intents(request.prompt)
        plan = generate_plan(intents, kb, tool_manager)
        
        executed_steps = []
        for i in range(MAX_ITERATIONS):
            if not plan:
                break

            step = plan.pop(0)
            try:
                result, error = execute_step(step, kb, tool_manager)
            except Exception as step_error:
                logging.error(f"Error in step {i+1}: {str(step_error)}")
                result = None
                error = str(step_error)

            executed_steps.append({"step": step, "result": result, "error": error})

            if error:
                # Attempt to recover by regenerating plan
                try:
                    plan = generate_plan(intents, kb, tool_manager, executed_steps, error)
                except Exception as plan_error:
                    logging.error(f"Failed to regenerate plan: {str(plan_error)}")
                    # Continue with remaining plan or break
                    continue
            if not plan:
                break

        # learn_from_execution(executed_steps, kb)
        evaluation_score = evaluate_plan_execution(executed_steps)

        return {
            "status": "success",
            "message": "Elch has executed the plan successfully.",
            "steps": executed_steps,
            "evaluation_score": evaluation_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))