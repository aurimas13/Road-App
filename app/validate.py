from urllib import parse
from app.data_validation import RequestValidate
from marshmallow import ValidationError


def validate_input(url):
    request_dict = dict(
        parse.parse_qsl(
            parse.urlsplit(url).query
        )
    )
    try:
        RequestValidate().load(request_dict)
    except ValidationError:
        raise ValidationError("The query parameter sent were incorrect")
