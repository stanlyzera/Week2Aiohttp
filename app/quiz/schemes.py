from marshmallow import Schema, fields


class ThemeSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Boolean()


class QuestionSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema))


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class ThemeIdSchema(Schema):
    id = fields.Int()


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)
