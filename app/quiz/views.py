from aiohttp.web_exceptions import HTTPConflict
from aiohttp_apispec import (docs, querystring_schema, request_schema,
                             response_schema)
from app.quiz.models import Answer
from app.quiz.schemes import (ListQuestionSchema, QuestionSchema,
                              ThemeIdSchema, ThemeListSchema, ThemeSchema)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @docs(tags=["Quiz"], summary="Add theme")
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema, 200)
    async def post(self):
        data = self.request['data']
        title = data["title"]
        themeb = await self.store.quizzes.get_theme_by_title(title)
        if themeb and title == themeb.title:
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @docs(tags=["Quiz"], summary="Get theme list")
    @response_schema(ThemeListSchema, 200)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=["Quiz"], summary="Add Question")
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema, 200)
    async def post(self):
        data = self.request['data']
        answers = [Answer.dict_converter(answer) for answer in self.data["answers"]]
        question = await self.request.app.store.quizzes.create_question(
                title=data["title"],
                theme_id=data["theme_id"],
                answers=answers
        )
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @docs(tags=["Quiz"], summary="List questions")
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema, 200)
    async def get(self):
        theme_id = (
            int(self.request.query.get("theme_id"))
            if self.request.query.get("theme_id")
            else None
        )
        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(data={"questions": [QuestionSchema().dump(question) for question in questions]})
