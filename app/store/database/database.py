from dataclasses import dataclass, field
from app.admin.models import Admin

from app.quiz.models import Question, Theme


@dataclass
class Database:
    admins: list[Admin] = field(default_factory=list)
    themes: list[Theme] = field(default_factory=list)
    sessions: dict[str, int] = field(default_factory=dict)
    questions: list[Question] = field(default_factory=list)

    @property
    def next_theme_id(self) -> int:
        return len(self.themes) + 1

    @property
    def next_admin_id(self) -> int:
        return len(self.admins) + 1

    @property
    def next_question_id(self) -> int:
        return len(self.questions) + 1

    def clear(self):
        self.admins.clear()
        self.themes.clear()
        self.sessions.clear()
        self.questions.clear()

    async def get_session_func(self, session_id: str):
        return self.sessions.get(session_id, None)
