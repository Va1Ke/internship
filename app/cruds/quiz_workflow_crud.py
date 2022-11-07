from fastapi import HTTPException
from datetime import datetime, timedelta
from sqlalchemy import and_
from app.schemas import company_schemas, requst_from_user_schemas, user_of_company_schemas, quiz_workflow_schemas
from app.models.models import companies, quizzes, quiz_questions, quiz_workflows, quiz_answers, users_of_companys
from app.cruds.quiz_crud import crud as quiz_crud
from app.database import db

class QuizWorkFlow_crud:

    async def show_quiz_questions(self, quiz_id: int) -> list:
        query = quiz_questions.select().where(quiz_questions.c.quiz_id == quiz_id)
        list = await db.fetch_all(query=query)
        if list == None:
            return None
        return [quiz_workflow_schemas.QuizWorkFlowQuestionsReturn(**request) for request in list]

    async def update_user_of_company(self, company_id: int, user_id: int):
        rights = 0
        questions = 0
        last_time = datetime.now() - timedelta(days=1000)
        query = quiz_workflows.select().where(and_(quiz_workflows.c.company_id == company_id, quiz_workflows.c.user_id == user_id))
        user_list = await db.fetch_all(query=query)
        for user in user_list:
            user_details = quiz_workflow_schemas.QuizWorkFlowReturn(**user)
            rights = rights + user_details.right_answers
            questions = questions + user_details.count_of_questions
            if user_details.time > last_time:
                last_time = user_details.time

        avg_result = rights/questions

        query = (users_of_companys.update().where(and_(users_of_companys.c.company_id == company_id, users_of_companys.c.user_id == user_id)).values(
            avg_result=avg_result,
            last_time_quiz=last_time
        ).returning(users_of_companys.c.id))
        record_id = await db.execute(query=query)

        return user_of_company_schemas.UserOfCompanyReturn(id=record_id, company_id=company_id, user_id=user_id, is_admin=True, avg_result=avg_result, time=last_time)

    async def enter_questions_answers(self, answers: quiz_workflow_schemas.QuizWorkFlowEntering, user_id: int, quiz_id: int, company_id: int):
        k = 0
        right = 0

        for i in answers.dict()["answers"]:
            query = quiz_answers.select().where(quiz_answers.c.question_id == i["question_id"])
            question = await db.fetch_one(query=query)
            k = k+1
            if question.answer is i["answer"]:
                right = right + 1

        result = right/k

        db_result = quiz_workflows.insert().values(user_id=user_id, company_id=company_id, quiz_id=quiz_id, result=result, right_answers=right, count_of_questions=k, time=datetime.now())
        record_id = await db.execute(db_result)
        await self.update_user_of_company(company_id=company_id, user_id=user_id)
        return quiz_workflow_schemas.QuizWorkFlowReturn(id=record_id, user_id=user_id, company_id=company_id, quiz_id=quiz_id, result=result, right_answers=right, count_of_questions=k, time=datetime.now())


crud = QuizWorkFlow_crud()