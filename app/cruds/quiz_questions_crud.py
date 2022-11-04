from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from app.cruds.quiz_questions_answers_crud import crud as quiz_questions_answers_crud
from app.schemas import quiz_questions_schemas
from app.models.models import quizzes, quiz_questions
from app.database import db

class QuizQuestions_crud:

    async def add_question(self, question: quiz_questions_schemas.QuizQuestionEntry):
        db_company = quiz_questions.insert().values(quiz_id=question.quiz_id, description=question.description)
        record_id = await db.execute(db_company)
        return quiz_questions_schemas.QuizQuestionReturn(**question.dict(), id=record_id)

    async def get_question_by_id(self, id: int):
        quiz = await db.fetch_one(quiz_questions.select().where(quiz_questions.c.id == id))
        if quiz == None:
            return None
        return quiz_questions_schemas.QuizQuestionReturn(**quiz)

    async def delete_question_for_quiz_crud(self, quiz_id: int) -> HTTPException:
        query = quiz_questions.select().where(quiz_questions.c.quiz_id == quiz_id)
        list = await db.fetch_all(query=query)
        for question in list:
            quest = quiz_questions_schemas.QuizQuestionReturn(**question)
            await quiz_questions_answers_crud.delete_answer_for_question_for_crud(question_id=quest.id)

        query = quiz_questions.delete().where(quiz_questions.c.quiz_id == quiz_id)
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def delete_question(self, quiz_id: int, question_id: int) -> HTTPException:
        query = quiz_questions.select().where(and_(quiz_questions.c.quiz_id == quiz_id, quiz_questions.c.id == question_id))
        question = await db.fetch_one(query=query)
        await quiz_questions_answers_crud.delete_answer_for_question_for_crud(question_id=question.id)

        query = quiz_questions.delete().where(quiz_questions.c.quiz_id == quiz_id)
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

crud = QuizQuestions_crud()