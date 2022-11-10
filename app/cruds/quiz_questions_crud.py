from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from app.cruds.quiz_questions_answers_crud import QuizQuestionAnswer
from app.schemas import quiz_questions_schemas
from app.models.models import quiz_questions
import databases

class QuizQuestions_crud:
    def __init__(self, db: databases.Database):
        self.db = db

    async def add_question(self, question: quiz_questions_schemas.QuizQuestionEntry) -> quiz_questions_schemas.QuizQuestionReturn:
        db_company = quiz_questions.insert().values(quiz_id=question.quiz_id, description=question.description)
        record_id = await self.db.execute(db_company)
        return quiz_questions_schemas.QuizQuestionReturn(**question.dict(), id=record_id)

    async def get_question_by_id(self, id: int) -> quiz_questions_schemas.QuizQuestionReturn:
        quiz = await self.db.fetch_one(quiz_questions.select().where(quiz_questions.c.id == id))
        if quiz == None:
            return None
        return quiz_questions_schemas.QuizQuestionReturn(**quiz)

    async def delete_question_for_Quiz_crud(self, quiz_id: int) -> HTTPException:
        query = quiz_questions.select().where(quiz_questions.c.quiz_id == quiz_id)
        list = await self.db.fetch_all(query=query)
        for question in list:
            quest = quiz_questions_schemas.QuizQuestionReturn(**question)
            await QuizQuestionAnswer(db=db).delete_answer_for_question_for_crud(question_id=quest.id)

        query = quiz_questions.delete().where(quiz_questions.c.quiz_id == quiz_id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def delete_question(self, quiz_id: int, question_id: int) -> HTTPException:
        query = quiz_questions.select().where(and_(quiz_questions.c.quiz_id == quiz_id, quiz_questions.c.id == question_id))
        question = await self.db.fetch_one(query=query)
        await QuizQuestionAnswer(db=db).delete_answer_for_question_for_crud(question_id=question.id)

        query = quiz_questions.delete().where(quiz_questions.c.quiz_id == quiz_id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

#crud = QuizQuestions_crud()