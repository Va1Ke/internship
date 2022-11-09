from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.utils.utils import get_email_from_token
from app.config import settings
from app.schemas import quiz_workflow_schemas
from app.cruds.company_crud import crud as company_crud
from app.cruds.quiz_crud import crud as quiz_crud
from app.cruds.quiz_workflow_crud import crud as quiz_workflow_crud
from app.cruds.crud import crud as user_crud
from app.database import db

router = APIRouter()

@router.post("/get-quiz-questions/", tags=["quiz_workflow"], response_model=list[quiz_workflow_schemas.QuizWorkFlowQuestionsReturn])
async def get_quiz_questions(quiz_id: int, email: str = Depends(get_email_from_token)) -> list[quiz_workflow_schemas.QuizWorkFlowQuestionsReturn]:
    owner = await user_crud.get_user_by_email(email,db=db)
    quiz = await quiz_crud.get_quiz_by_id(quiz_id,db=db)
    company = await company_crud.get_company_by_id(quiz.company_id,db=db)
    is_user_in_company = await company_crud.check_is_user_in_company(company_id=company.id, user_id=owner.id,db=db)
    if is_user_in_company == True:
        return await quiz_workflow_crud.show_quiz_questions(quiz_id=quiz_id,db=db)
    else:
        raise HTTPException(status_code=400, detail="No permission")

@router.post("/enter-answers/", tags=["quiz_workflow"], response_model=quiz_workflow_schemas.QuizWorkFlowReturn)
async def enter_answers(quiz_id: int, answers: quiz_workflow_schemas.QuizWorkFlowEntering, email: str = Depends(get_email_from_token)) -> quiz_workflow_schemas.QuizWorkFlowReturn:
    owner = await user_crud.get_user_by_email(email,db=db)
    quiz = await quiz_crud.get_quiz_by_id(quiz_id,db=db)
    company = await company_crud.get_company_by_id(quiz.company_id,db=db)
    is_user_in_company = await company_crud.check_is_user_in_company(company_id=company.id, user_id=owner.id,db=db)
    if is_user_in_company:
        return await quiz_workflow_crud.enter_questions_answers(answers=answers, user_id=owner.id, quiz_id=quiz_id, company_id=company.id,db=db)
    else:
        raise HTTPException(status_code=400, detail="No permission")