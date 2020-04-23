from unittest import TestCase
from .datecore import Date, DateFormat
from datetime import date
import arrow


class TestDate(TestCase):

    def setUp(self) -> None:
        self.date = date(2020, 4, 19)
        self.arrow_date = Date(self.date)

    def test_change_to_arrow(self):
        self.assertEqual(type(self.arrow_date.date), arrow.arrow.Arrow)

    def test_nice_date_normal(self):
        self.arrow_date.date_format = DateFormat.NORMAL
        self.assertEqual(self.arrow_date.nice_date, 'Sunday, the 19th of April')

    def test_nice_date_normal_year(self):
        self.arrow_date.date_format = DateFormat.NORMAL_YEAR
        self.assertEqual(self.arrow_date.nice_date, 'Sunday, the 19th of April, 2020')

    def test_create_message(self):
        self.arrow_date.date_format = DateFormat.NORMAL
        template = self.arrow_date.env.get_template('today.message')
        messages = template.render(user="Linus", date=self.arrow_date.nice_date).split('\n')
        self.assertIn(self.arrow_date.create_message("Linus"), messages)
