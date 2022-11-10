from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas import quiz_workflow_schemas
from app.cruds.company_crud import Company_crud
from app.cruds.quiz_crud import Quiz_crud
from app.cruds.quiz_workflow_crud import QuizWorkFlow_crud
from app.cruds.crud import Cruds
from app.database import db, test_db

router = APIRouter()

@router.post("/get-quiz-questions/", tags=["quiz_workflow"], response_model=list[quiz_workflow_schemas.QuizWorkFlowQuestionsReturn])
async def get_quiz_questions(quiz_id: int, email: str = Depends(get_email_from_token)) -> list[quiz_workflow_schemas.QuizWorkFlowQuestionsReturn]:
    owner = await Cruds(db=db).get_user_by_email(email)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(quiz_id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    is_user_in_company = await Company_crud(db=db).check_is_user_in_company(company_id=company.id, user_id=owner.id)
    if is_user_in_company == True:
        return await QuizWorkFlow_crud(db=db).show_quiz_questions(quiz_id=quiz_id)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/enter-answers/", tags=["quiz_workflow"], response_model=quiz_workflow_schemas.QuizWorkFlowReturn)
async def enter_answers(quiz_id: int, answers: quiz_workflow_schemas.QuizWorkFlowEntering, email: str = Depends(get_email_from_token)) -> quiz_workflow_schemas.QuizWorkFlowReturn:
    owner = await Cruds(db=db).get_user_by_email(email)
    quiz = await Quiz_crud(db=db).get_quiz_by_id(quiz_id)
    company = await Company_crud(db=db).get_company_by_id(quiz.company_id)
    is_user_in_company = await Company_crud(db=db).check_is_user_in_company(company_id=company.id, user_id=owner.id)
    if is_user_in_company:
        return await QuizWorkFlow_crud(db=db).enter_questions_answers(answers=answers, user_id=owner.id, quiz_id=quiz_id, company_id=company.id)
    else:
        raise HTTPException(status_code=400, detail="No permission")