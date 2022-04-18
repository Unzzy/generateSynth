import datetime
import random


def str_to_datetime(string_for_format, format_date):
    return datetime.datetime.strptime(string_for_format, format_date)


def number_generate(min_value, max_value) -> int:
    return random.randint(min_value, max_value)


def date_generate(begin_date, end_date, date_format) -> datetime:
    start = str_to_datetime(begin_date, date_format)
    end = str_to_datetime(end_date, date_format)
    result_time = start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )
    return result_time


def string_generate(min_length, max_length, characters) -> str:
    return ''.join(characters[random.randint(0, len(characters) - 1)]
                   for i in range(0, random.randint(min_length, max_length)))

