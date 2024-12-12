from .routes import app
from .utils import logging
from . import database
import uuid
import random


def test():
    logging.info("Test starting")
    database.reset()
    option_count_real = database.get_option_count()
    combinations_real = 0
    random_user_count = 10
    for a in range(0, option_count_real):
        for _ in range(0, a):
            combinations_real += 1
    combinations = min(50, combinations_real)
    logging.info(f"option_count (real): {option_count_real}")
    logging.info(f"combinations (real): {combinations_real}")
    logging.info(f"combinations (used): {combinations}")
    auid_a = "a3f5a16d-f39e-4c47-b2c6-d7811f229d33"
    database.add_anonymous_user(auid_a, "Anon A")
    for _ in range(0, combinations):
        choice = "a"
        x = database.get_anonymous_question({
            "auid": auid_a
        })[0]
        database.set_anonymous_answer({
            "user_id": auid_a,
            "a": x['a'],
            "b": x['b'],
            "choice": choice,
        })
    auid = "b3f5a16d-f39e-4c47-b2c6-d7811f229d33"
    database.add_anonymous_user(auid, "Anon B")
    for _ in range(0, combinations):
        choice = "b"
        x = database.get_anonymous_question({
            "auid": auid
        })[0]
        database.set_anonymous_answer({
            "user_id": auid,
            "a": x['a'],
            "b": x['b'],
            "choice": choice,
        })
    for a in range(0, random_user_count):
        logging.info(f"user #{a}")
        auid = str(uuid.uuid4())
        database.add_anonymous_user(auid, f"Anon #{a}")
        for b in range(0, combinations):
            r = random.randint(0, 1)
            choice = ["a", "b"][r]
            x = database.get_anonymous_question({
                "auid": auid
            })[0]
            database.set_anonymous_answer({
                "user_id": auid,
                "a": x['a'],
                "b": x['b'],
                "choice": choice,
            })
    database.get_anonymous_matches({"user_id": auid_a})
    x = database.get_anonymous_ranking({"user_id":auid})
    logging.info("Test ok")


test()
