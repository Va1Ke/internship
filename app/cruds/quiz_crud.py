from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from app.cruds.quiz_questions_crud import crud as quiz_questions_crud
from app.schemas import quiz_schemas
from app.models.models import companies, users_of_companys, quizzes
from app.database import db

class Quiz_crud:

    async def create_quiz(self, quiz: quiz_schemas.QuizEntry) -> quiz_schemas.QuizReturn:
        db_company = quizzes.insert().values(company_id=quiz.company_id, name=quiz.name, description=quiz.description)
        record_id = await db.execute(db_company)
        return quiz_schemas.QuizReturn(**quiz.dict(), id=record_id)

    async def get_quiz_by_id(self, id: int) -> quiz_schemas.QuizReturn:
        quiz = await db.fetch_one(quizzes.select().where(quizzes.c.id == id))
        if quiz == None:
            return None
        return quiz_schemas.QuizReturn(**quiz)

    async def update_quiz(self, quiz: quiz_schemas.QuizUpdateEntry) -> quiz_schemas.QuizReturn:
        query = (quizzes.update().where(quizzes.c.id == quiz.id).values(
            name=quiz.name,
            description=quiz.description,

        ).returning(companies.c.company_id))
        company_id = await db.execute(query=query)
        return quiz_schemas.QuizReturn(**quiz.dict(), company_id=company_id)

    async def delete_quiz(self, quiz_id: int) -> HTTPException:
        await quiz_questions_crud.delete_question_for_quiz_crud(quiz_id)

        query = quizzes.delete().where(quizzes.c.id == quiz_id)
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def show_quizzes_in_company(self, company_id: int) -> list[quiz_schemas.QuizReturn]:
        query = quizzes.select().where(quizzes.c.company_id == company_id)
        list = await db.fetch_all(query=query)
        if list == None:
            return None
        return [quiz_schemas.QuizReturn(**request) for request in list]

crud = Quiz_crud()