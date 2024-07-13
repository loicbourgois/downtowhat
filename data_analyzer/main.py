from .log import logging

logging.info("start")
import os
import pandas
import datetime
import json
import pandasql
import glob
import hashlib


def cleanup(df):
    def transform(row):
        try:
            row["qid"] = hashlib.sha256(
                str(f"{row['question']} | {row['a']} | {row['b']}").encode("utf-8")
            ).hexdigest()
            row["json_response"] = row["json_response"].replace("\\n", "\n")
            row["parsed_response"] = ""
            row["answer"] = ""
            row["parsed_response"] = json.loads(row["json_response"])
            answer = row["parsed_response"]["answer"]
            if (
                row["a"].lower() in answer.lower()
                and row["b"].lower() not in answer.lower()
            ):
                row["answer"] = row["a"]
            elif (
                row["a"].lower() not in answer.lower()
                and row["b"].lower() in answer.lower()
            ):
                row["answer"] = row["b"]
        except Exception as e:
            pass
            # logging.error(e)
        return row

    df = df.apply(transform, axis=1)
    return df


def compute_similarity(df):
    similarities = []
    personas = set(df["persona"].unique())
    for p1 in personas:
        for p2 in personas:
            if p1 != p2:
                similarity_count = pandasql.sqldf(
                    f"""
                    with q1 as (
                        select * from df
                        where df.persona = '{p1}'
                    ),
                    q2 as (
                        select * from df
                        where df.persona = '{p2}'
                    )
                    select count(*) as similarity_count
                    from q1
                    inner join q2
                    on q1.qid = q2.qid
                        and q1.answer = q2.answer
                        and q1.answer != ''
                """,
                    locals(),
                ).similarity_count[0]
                question_count = pandasql.sqldf(
                    f"""
                    with q1 as (
                        select distinct qid from df
                        where (persona = '{p1}' or persona = '{p2}')
                            and answer != ''
                    )
                    select count(*) as question_count
                    from q1
                """,
                    locals(),
                ).question_count[0]
                question_count_1 = pandasql.sqldf(
                    f"""
                    with q1 as (
                        select distinct qid from df
                        where persona = '{p1}'
                            and answer != ''
                    )
                    select count(*) as question_count_1
                    from q1
                """,
                    locals(),
                ).question_count_1[0]
                question_count_2 = pandasql.sqldf(
                    f"""
                    with q1 as (
                        select distinct qid from df
                        where persona = '{p1}'
                            and answer != ''
                    )
                    select count(*) as question_count_2
                    from q1
                """,
                    locals(),
                ).question_count_2[0]
                similarities.append(
                    {
                        "p1": p1,
                        "p2": p2,
                        "similaritty": similarity_count / question_count,
                        "similarity_count": similarity_count,
                        "question_count": question_count,
                        "qc1": question_count_1,
                        "qc2": question_count_2,
                    }
                )
    similarities_df = pandas.DataFrame(similarities)
    return similarities_df


paths = glob.glob(
    f"{os.environ['HOME']}/github.com/loicbourgois/downtowhat/data_builder/archive/*.csv"
)
columns = ["qid", "persona", "answer"]
df = pandas.DataFrame(columns=columns)
for path in paths:
    df_tmp = pandas.read_csv(
        path,
        delimiter=",",
        dtype="string",
    )
    df_tmp = cleanup(df_tmp)
    try:
        df = pandas.concat([df, df_tmp[df.columns]], ignore_index=True)
    except Exception as e:
        pass
for k in list(df.columns):
    df[k] = df[k].astype("string")

logging.info(df.size)
df = df.drop_duplicates()
logging.info(df.size)

similarities = compute_similarity(df)


with pandas.option_context(
    "display.max_columns", 400, "display.max_rows", None, "display.width", 400
):
    logging.info(
        pandasql.sqldf(
            f"""
        select p1,p2, similaritty 
        from similarities
        -- where p1 = 'Stalin'
        order by p1, similaritty desc
    """,
            locals(),
        )
    )
    # logging.info(pandasql.sqldf(f"""
    #     select p1,p2, similaritty
    #     from similarities
    #     where p1 = 'a young lady from LA'
    #     order by similaritty desc
    # """, locals()))
