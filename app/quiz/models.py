from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Theme:
    id: Optional[int]
    title: str


@dataclass
class Answer:
    title: str
    is_correct: bool

    @classmethod
    def dict_converter(cls, dic: dict):
        return cls(title=dic['title'], is_correct=dic['is_correct'])


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list[Answer] = field(default_factory=list)
