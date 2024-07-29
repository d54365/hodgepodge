from django.test import TestCase

from common.utils.random import RandomUtil


class RandomUtilTestCase(TestCase):
    def test_generate_number(self):
        number = RandomUtil.generate_number(6)
        self.assertEqual(len(number), 6)
        self.assertTrue(number.isdigit())

    def test_generate(self):
        random_string = RandomUtil.generate(8)
        self.assertEqual(len(random_string), 8)
        self.assertTrue(any(c.isalpha() for c in random_string))
