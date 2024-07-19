from .utils.database import (
    query_to_dicts,
    run_query,
    new_database_engine,
)
from .utils.files import read
import uuid


db_engine = new_database_engine(
    user="dtw_local_dev_user",
    password="dtw_local_dev_password",
    host="host.docker.internal",
    port="5432",
    database="dtw_local_dev",
    socket="",
)


def reset():
    test_user_id = '13f5a16d-f39e-4c47-b2c6-d7811f229d13'
    try:
        add_anonymous_user(test_user_id)
    except:
        pass
    run_query(
        engine = db_engine,
        query = """
            delete 
            from anonymous_response 
            where user_id != :user_id;
        """,
        args = {
            "user_id": test_user_id
        }
    )
    run_query(
        engine = db_engine,
        query = """
            delete 
            from anonymous_dtw_user
            where user_id != :user_id;
        """,
        args = {
            "user_id": test_user_id
        }
    )


get_anonymous_question_query = read("/root/github.com/loicbourgois/downtowhat/app/queries/get_anonymous_question.sql")
def get_anonymous_question(x):
    return query_to_dicts(
        engine = db_engine,
        query = get_anonymous_question_query,
        args = {
            "user_id": x['auid']
        }
    )


def get_option_count():
    return int(query_to_dicts(
        engine = db_engine,
        query = """
            select count(*) as c from option
        """,
    )[0]['c'])



def set_anonymous_answer(x):
    return run_query(
        engine = db_engine,
        query = """
            insert into anonymous_response (user_id, a, b, choice)
            values (:user_id, :a, :b, :choice)
        """,
        args = x,
    )


def reset_anonymous_option(x):
    return run_query(
        engine = db_engine,
        query = """
            delete from anonymous_response
            where 
                user_id = :user_id
                and (
                    a = :option_id
                    or b = :option_id
                )
        """,
        args = x,
    )


def add_anonymous_user(user_id=None, username="Anon"):
    if not user_id:
        user_id = str(uuid.uuid4())
    run_query(
        engine = db_engine,
        query = """
            insert into anonymous_dtw_user (user_id, public_user_id, username)
            values (:user_id, :public_user_id, :username)
        """,
        args = {
            "user_id": user_id,
            "username": username,
            "public_user_id": str(uuid.uuid4()),
        }
    )
    return user_id


get_anonymous_ranking_query = read("/root/github.com/loicbourgois/downtowhat/app/queries/get_anonymous_ranking.sql")
def get_anonymous_ranking(x):
    return {
        "username": query_to_dicts(
            engine = db_engine,
            query = """
                select username 
                from anonymous_dtw_user
                where user_id = :user_id
            """,
            args = x,    
        ),
        "rankings": query_to_dicts(
            engine = db_engine,
            query = get_anonymous_ranking_query,
            args = x,
        )
    }


get_anonymous_ranking_2_query = read("/root/github.com/loicbourgois/downtowhat/app/queries/get_anonymous_ranking_2.sql")
get_anonymous_match_single_query = read("/root/github.com/loicbourgois/downtowhat/app/queries/get_anonymous_match_single.sql")
def get_anonymous_ranking_2(x):
    return {
        "username": query_to_dicts(
            engine = db_engine,
            query = """
                select username 
                from anonymous_dtw_user
                where public_user_id = :public_user_id
            """,
            args = x,    
        ),
        "rankings": query_to_dicts(
            engine = db_engine,
            query = get_anonymous_ranking_2_query,
            args = x,    
        ),
        "score": query_to_dicts(
            engine = db_engine,
            query = get_anonymous_match_single_query,
            args = x,    
        ),
    }


get_anonymous_matches_query = read("/root/github.com/loicbourgois/downtowhat/app/queries/get_anonymous_matches.sql")
def get_anonymous_matches(x):
    return query_to_dicts(
        engine = db_engine,
        query = get_anonymous_matches_query,
        args = x,
    )