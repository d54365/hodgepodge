import random
import string


class RandomUtil:
    @staticmethod
    def generate_number(length: int):
        return "".join(random.sample(string.digits, length))

    @staticmethod
    def generate(length: int):
        return "".join(
            random.sample(
                f"{string.digits}{string.ascii_letters}{string.punctuation}", length
            )
        )
