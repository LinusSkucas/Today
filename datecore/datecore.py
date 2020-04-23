from datetime import date
from enum import Enum
import arrow
from jinja2 import Environment, PackageLoader
from random import choice


class DateFormat(Enum):
    NORMAL = "dddd[, the ]Do [of] MMMM"
    NORMAL_YEAR = "dddd[, the ]Do [of] MMMM[, ]YYYY"


class Date:
    def __init__(self, date: date = date.today(), date_format: DateFormat = DateFormat.NORMAL):
        """
        :type date: date
        :type date_format: DateFormat
        """
        self.date = arrow.get(date)
        self.date_format = date_format

        self.env = Environment(loader=PackageLoader('datecore', 'templates'))

    @property
    def nice_date(self) -> str:
        return self.date.format(self.date_format.value)

    def create_message(self, user: str) -> str:
        template = self.env.get_template('today.message')
        messages = template.render(user=user, date=self.nice_date).split('\n')
        return choice(messages)
