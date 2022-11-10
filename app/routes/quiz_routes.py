from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas.quiz_schemas import *
import http.client
from datetime import timedelta
from app.schemas import company_schemas, quiz_questions_schemas, quiz_question_answers_schemas
from app.cruds.company_crud import Company_crud
from app.cruds.quiz_crud import Quiz_crud
from app.cruds.crud import Cruds
from app.cruds.quiz_questions_crud import QuizQuestions_crud
from app.cruds.quiz_questions_answers_crud import QuizQuestionAnswer
from app.database import db, test_db


router = APIRouter()


@router.post("/create-quiz/", tags=["quiz"], response_model=QuizReturn)
async def create(quiz: QuizEntry, email: str = Depends(get_email_from_token)) -> QuizReturn:
    owner = await Cruds(db=db).get_user_by_email(email)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await Quiz_crud(db=db).create_quiz(quiz)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/show-quizzes-by-company/", tags=["quiz"], response_model=list[QuizReturn])
async def get_quizzes_by_company(company_id: int, email: str = Depends(get_email_from_token)) -> list[QuizReturn]:
    owner = await Cruds(db=db).get_user_by_email(email)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await Quiz_crud(db=db).show_quizzes_in_company(company_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.put("/update-quiz/", tags=["quiz"], response_model=QuizReturn)
async def create(quiz_entry: QuizUpdateEntry, email: str = Depends(get_email_from_token)) -> QuizReturn:
    owner = await Cruds(db=db).get_user_by_email(email)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(quiz_entry.id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await Quiz_crud(db=db).update_quiz(quiz_entry)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-quiz/", tags=["quiz"])
async def create(quiz_id: int, email: str = Depends(get_email_from_token)):
    owner = await Cruds(db=db).get_user_by_email(email)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(quiz_id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await Quiz_crud(db=db).delete_quiz(quiz_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/add-question-to-quiz/", tags=["quiz"], response_model=quiz_questions_schemas.QuizQuestionReturn)
async def add_question(question: quiz_questions_schemas.QuizQuestionEntry, email: str = Depends(get_email_from_token)) -> quiz_questions_schemas.QuizQuestionReturn:
    owner = await Cruds(db=db).get_user_by_email(email)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(question.quiz_id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await QuizQuestions_crud(db=db).add_question(question)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-question-from-quiz/", tags=["quiz"])
async def create(quiz_id: int, question_id: int, email: str = Depends(get_email_from_token)):
    owner = await Cruds(db=db).get_user_by_email(email)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(quiz_id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await QuizQuestions_crud(db=db).delete_question(quiz_id=quiz_id,question_id=question_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/add-answer-to-question/", tags=["quiz"], response_model=quiz_question_answers_schemas.QuizQuestionAnswerReturn)
async def add_question(answer: quiz_question_answers_schemas.QuizQuestionAnswerEntry, email: str = Depends(get_email_from_token)) -> quiz_question_answers_schemas.QuizQuestionAnswerReturn:
    owner = await Cruds(db=db).get_user_by_email(email)
    question = await QuizQuestions_crud(db=db).get_question_by_id(answer.question_id)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(question.quiz_id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await QuizQuestionAnswer(db=db).add_answer(answer)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.delete("/delete-answer-from-question/", tags=["quiz"])
async def create(answer_id: int, question_id: int, email: str = Depends(get_email_from_token)):
    owner = await Cruds(db=db).get_user_by_email(email)
    question = await QuizQuestions_crud(db=db).get_question_by_id(question_id)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(question.quiz_id)
    check_is_admin = await Company_crud(db=db).check_is_admin(company_id=quiz.company_id, user_id=owner.id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    if company.owner_id == owner.id or check_is_admin == True:
        return await QuizQuestionAnswer(db=db).delete_answer(answer_id=answer_id, question_id=question_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")