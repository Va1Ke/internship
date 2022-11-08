from fastapi import HTTPException
from datetime import datetime, date
from sqlalchemy import and_
from operator import itemgetter
from app.cruds.quiz_questions_crud import crud as quiz_questions_crud
from app.schemas import quiz_schemas, user_of_company_schemas, schemas, quiz_workflow_schemas
from app.models.models import companies, users_of_companys, quizzes, users, quiz_workflows
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

    async def show_result_of_user(self, user_id: int) -> list[quiz_schemas.QuizReturn]:
        query = users_of_companys.select().where(users_of_companys.c.user_id == user_id)
        list = await db.fetch_all(query=query)
        if list:
            k = 0
            avg_all = 0.0
            last_time_quiz = date(2000, 9, 9)
            for user in list:
                avg_all = avg_all + user.avg_result
                k = k+1
                if user.last_time_quiz.date() > last_time_quiz:
                    last_time_quiz = user.last_time_quiz

            avg = avg_all/k
            query = users.select().where(users.c.id == user_id)
            user = await db.fetch_one(query=query)

            return schemas.UserAvgAll(**user, avg_quiz_result=avg, last_time_quiz=last_time_quiz)
        else:
            raise HTTPException(status_code=400, detail="No such user")

    async def show_quiz_result_by_user(self, quiz_id: int, user_id: int):
        query = quiz_workflows.select().where(and_(quiz_workflows.c.quiz_id == quiz_id, quiz_workflows.c.user_id == user_id))
        list = await db.fetch_all(query=query)
        if list:
            sorted_list = sorted(list, key=itemgetter('time'))
            k = 0
            avg_all = 0.0
            returned_list = []
            for item in sorted_list:
                user = quiz_workflow_schemas.QuizWorkFlowReturn(**item)
                avg_all = avg_all + user.result
                k = k+1
                avg = avg_all / k
                dict = {avg: user.time}
                returned_list.append(dict)

            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")

    async def show_user_quiz_list(self, user_id: int):
        query = quiz_workflows.select().where(quiz_workflows.c.user_id == user_id)
        list = await db.fetch_all(query=query)
        if list:
            sorted_list = sorted(list, key=itemgetter('time'))

            returned_list = []
            for item in sorted_list:
                user = quiz_workflow_schemas.QuizWorkFlowReturn(**item)
                dict = {user.quiz_id: user.time}
                returned_list.append(dict)

            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")


crud = Quiz_crud()