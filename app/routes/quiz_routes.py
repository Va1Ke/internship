from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.quiz_schemas import *
import http.client
from datetime import timedelta
from app.schemas import company_schemas, quiz_questions_schemas, quiz_question_answers_schemas
from app.cruds.company_crud import crud as company_crud
from app.cruds.quiz_crud import crud as quiz_crud
from app.cruds.crud import crud as user_crud
from app.cruds.quiz_questions_crud import crud as quiz_questions_crud
from app.cruds.quiz_questions_answers_crud import crud as quiz_questions_answers_crud


router = APIRouter()


@router.post("/create-quiz/", tags=["quiz"], response_model=QuizReturn)
async def create(quiz: QuizEntry, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    check_is_admin = await company_crud.check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_crud.create_quiz(quiz)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/show-quizzes-by-company/", tags=["quiz"], response_model=list[QuizReturn])
async def get_quizzes_by_company(company_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    check_is_admin = await company_crud.check_is_admin(company_id=company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_crud.show_quizzes_in_company(company_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.put("/update-quiz/", tags=["quiz"], response_model=QuizReturn)
async def create(quiz_entry: QuizUpdateEntry, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    quiz = await quiz_crud.get_quiz_by_id(quiz_entry.id)
    check_is_admin = await company_crud.check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_crud.update_quiz(quiz_entry)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-quiz/", tags=["quiz"])
async def create(quiz_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    quiz = await quiz_crud.get_quiz_by_id(quiz_id)
    check_is_admin = await company_crud.check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_crud.delete_quiz(quiz_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/add-question-to-quiz/", tags=["quiz"], response_model=quiz_questions_schemas.QuizQuestionReturn)
async def add_question(question: quiz_questions_schemas.QuizQuestionEntry, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    quiz = await quiz_crud.get_quiz_by_id(question.quiz_id)
    check_is_admin = await company_crud.check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_questions_crud.add_question(question)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-question-from-quiz/", tags=["quiz"])
async def create(quiz_id: int, question_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    quiz = await quiz_crud.get_quiz_by_id(quiz_id)
    check_is_admin = await company_crud.check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_questions_crud.delete_question(quiz_id=quiz_id,question_id=question_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/add-answer-to-question/", tags=["quiz"], response_model=quiz_question_answers_schemas.QuizQuestionAnswerReturn)
async def add_question(answer: quiz_question_answers_schemas.QuizQuestionAnswerEntry, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    question = await quiz_questions_crud.get_question_by_id(answer.question_id)
    quiz = await quiz_crud.get_quiz_by_id(question.quiz_id)
    check_is_admin = await company_crud.check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_questions_answers_crud.add_answer(answer)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-answer-from-question/", tags=["quiz"])
async def create(answer_id: int, question_id: int, email: str = Depends(get_email_from_token)):
    owner = await user_crud.get_user_by_email(email)
    question = await quiz_questions_crud.get_question_by_id(question_id)
    quiz = await quiz_crud.get_quiz_by_id(question.quiz_id)
    check_is_admin = await company_crud.check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await company_crud.get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await quiz_questions_answers_crud.delete_answer(answer_id=answer_id, question_id=question_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")