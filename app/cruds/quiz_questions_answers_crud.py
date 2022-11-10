from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from app.schemas import quiz_questions_schemas, quiz_question_answers_schemas
from app.models.models import quizzes, quiz_questions, quiz_answers
import databases

class QuizQuestionAnswer:
    def __init__(self, db: databases.Database):
        self.db = db

    async def add_answer(self, answer: quiz_question_answers_schemas.QuizQuestionAnswerEntry) -> quiz_question_answers_schemas.QuizQuestionAnswerReturn:
        db_company = quiz_answers.insert().values(answer=answer.answer, question_id=answer.question_id)
        record_id = await self.db.execute(db_company)
        return quiz_question_answers_schemas.QuizQuestionAnswerReturn(**answer.dict(), id=record_id)

    async def delete_answer_for_question_for_crud(self, question_id: int) -> HTTPException:
        query = quiz_answers.delete().where(quiz_answers.c.question_id == question_id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def delete_answer(self, answer_id: int, question_id: int) -> HTTPException:
        query = quiz_answers.delete().where(and_(quiz_answers.c.id == answer_id, quiz_answers.c.question_id == question_id))
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

#crud = QuizQuestionAnswer()