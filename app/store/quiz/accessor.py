from typing import Optional

from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from app.base.base_accessor import BaseAccessor
from app.quiz.models import Answer, Question, Theme


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        for i in self.app.database.themes:
            if i.title == title:
                return i

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        for i in self.app.database.themes:
            if i.id == id_:
                return i

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        for i in self.app.database.questions:
            if i.title == title:
                return i

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        if len(answers) < 2:
            raise HTTPBadRequest
        counter = [i for i in answers if i.is_correct is True]
        if len(counter) != 1:
            raise HTTPBadRequest
        if await self.get_question_by_title(title=title):
            raise HTTPNotFound
        if not (await self.get_theme_by_id(id_=theme_id)):
            raise HTTPNotFound
        question = Question(
            id=self.app.database.next_question_id,
            title=title,
            theme_id=theme_id,
            answers=answers,
        )
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        if theme_id:
            if theme_id not in [theme.id for theme in self.app.database.themes]:
                raise HTTPNotFound
            return [question for question in self.app.database.questions if question.theme_id == theme_id]
        return self.app.database.questions
