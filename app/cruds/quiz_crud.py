from fastapi import HTTPException
from datetime import datetime, date
from sqlalchemy import and_
from operator import itemgetter
from app.cruds.quiz_questions_crud import QuizQuestions_crud
from app.schemas import quiz_schemas, user_of_company_schemas, schemas, quiz_workflow_schemas, analitics_schemas
from app.models.models import companies, users_of_companys, quizzes, users, quiz_workflows
import databases

class Quiz_crud:
    def __init__(self, db: databases.Database):
        self.db = db

    async def create_quiz(self, quiz: quiz_schemas.QuizEntry) -> quiz_schemas.QuizReturn:
        db_company = quizzes.insert().values(company_id=quiz.company_id, name=quiz.name, description=quiz.description, frequency_of_passage=7)
        record_id = await self.db.execute(db_company)
        return quiz_schemas.QuizReturn(**quiz.dict(), id=record_id , frequency_of_passage=7, avg_result=0)

    async def get_quiz_by_id(self, id: int) -> quiz_schemas.QuizReturn:
        quiz = await self.db.fetch_one(quizzes.select().where(quizzes.c.id == id))
        return quiz_schemas.QuizReturn(**quiz) if quiz else None

    async def update_quiz(self, quiz: quiz_schemas.QuizUpdateEntry) -> quiz_schemas.QuizReturn:
        query = (quizzes.update().where(quizzes.c.id == quiz.id).values(
            name=quiz.name,
            description=quiz.description,

        ).returning(quizzes.c.company_id))
        company_id = await self.db.execute(query=query)
        return quiz_schemas.QuizReturn(**quiz.dict(), company_id=company_id)

    async def delete_quiz(self, quiz_id: int) -> HTTPException:
        await QuizQuestions_crud(db=self.db).delete_question_for_Quiz_crud(quiz_id)

        query = quizzes.delete().where(quizzes.c.id == quiz_id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def show_quizzes_in_company(self, company_id: int) -> list[quiz_schemas.QuizReturn]:
        query = quizzes.select().where(quizzes.c.company_id == company_id)
        list = await self.db.fetch_all(query=query)
        return [quiz_schemas.QuizReturn(**request) for request in list] if list else None

    async def show_result_of_user(self, user_id: int) -> list[analitics_schemas.UserResult]:
        query = quiz_workflows.select().where(quiz_workflows.c.user_id == user_id)
        list = await self.db.fetch_all(query=query)
        if list:
            sorted_list = sorted(list, key=itemgetter('time'))
            k = 0
            avg_all = 0.0
            returned_list = []
            for item in sorted_list:
                user = quiz_workflow_schemas.QuizWorkFlowReturn(**item)
                avg_all = avg_all + user.result
                k = k + 1
                avg = avg_all / k
                returned_list.append(analitics_schemas.UserResult(avg=avg, time=user.time))
            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")

    async def show_quiz_result_by_user(self, quiz_id: int, user_id: int) -> list[analitics_schemas.UserResult]:
        query = quiz_workflows.select().where(and_(quiz_workflows.c.quiz_id == quiz_id, quiz_workflows.c.user_id == user_id))
        list = await self.db.fetch_all(query=query)
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
                returned_list.append(analitics_schemas.UserResult(avg=avg,time=user.time))

            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")

    async def show_user_quiz_list(self, user_id: int) -> list[analitics_schemas.UserQuizList]:
        query = quiz_workflows.select().where(quiz_workflows.c.user_id == user_id)
        list = await self.db.fetch_all(query=query)
        if list:
            sorted_list = sorted(list, key=itemgetter('time'))

            returned_list = []
            for item in sorted_list:
                user = quiz_workflow_schemas.QuizWorkFlowReturn(**item)
                returned_list.append(analitics_schemas.UserQuizList(quiz_id=user.quiz_id,time=user.time))

            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")

    async def show_all_result_by_company(self, company_id: int) -> list[analitics_schemas.UserResult]:
        query = quiz_workflows.select().where(quiz_workflows.c.company_id == company_id)
        list = await self.db.fetch_all(query=query)
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
                returned_list.append(analitics_schemas.UserResult(avg=avg, time=user.time))

            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")

    async def show_all_result_by_company_and_user(self, company_id: int, user_id: int) -> list[analitics_schemas.UserResult]:
        query = quiz_workflows.select().where(and_(quiz_workflows.c.company_id == company_id, quiz_workflows.c.user_id == user_id))
        list = await self.db.fetch_all(query=query)
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
                returned_list.append(analitics_schemas.UserResult(avg=avg, time=user.time))

            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")

    async def list_user_of_company_and_last_time(self, company_id: int) -> list[analitics_schemas.ListUsersOfCompanyAndLastTime]:
        query = quiz_workflows.select().where(quiz_workflows.c.company_id == company_id)
        list = await self.db.fetch_all(query=query)
        if list:
            sorted_list = sorted(list, key=itemgetter('time'))
            returned_list = []
            for items in sorted_list:
                item = quiz_workflow_schemas.QuizWorkFlowReturn(**items)
                query = users_of_companys.select().where(users_of_companys.c.user_id == item.user_id)
                user = await self.db.fetch_one(query=query)
                user_to_add = user_of_company_schemas.UserOfCompanyReturnAvgAll(**user)
                returned_list.append(analitics_schemas.ListUsersOfCompanyAndLastTime(user_id=user_to_add.user_id, time=user_to_add.last_time_quiz))

            return returned_list
        else:
            raise HTTPException(status_code=400, detail="No such quiz")

#crud = Quiz_crud()