from .log import logging

from .oai import Openai
import os
import pandas
import datetime
from .parallel_v2 import (
    parallel_v2,
    async_wrap,
)
from .files import read

logging.info("start")

oai = Openai(
    api_key=os.environ["OPENAI_API_KEY"],
    organization=os.environ["OPENAI_ORGANIZATION"],
)

df = pandas.read_csv(
    f"{os.environ['HOME']}/github.com/loicbourgois/downtowhat/data_builder/questions.csv",
    delimiter=";",
    dtype="string",
)
questions_expanded = []
option_keys = list(df.columns)[2:]


def transform(row):
    for i, k1 in enumerate(option_keys[:-1]):
        for k2 in option_keys[i + 1 :]:
            if (
                type(row[k1]) == str
                and type(row[k2]) == str
                and len(row[k1])
                and len(row[k2])
            ):
                questions_expanded.append(
                    {
                        "question": row["question"],
                        "complimentary": row["complimentary"],
                        "a": row[k1],
                        "b": row[k2],
                    }
                )
    return row


df.apply(transform, axis=1)
pandas.DataFrame(questions_expanded).to_csv(
    f"{os.environ['HOME']}/github.com/loicbourgois/downtowhat/data_builder/questions_expanded.csv",
    index=False,
)
prompt = read(
    f"{os.environ['HOME']}/github.com/loicbourgois/downtowhat/data_builder/prompt.md"
)
data = []
for i in range(1):
    for persona in [
        "Hitler",
        "Kurt Cobain",
        "Barack Obama",
        "a young lady from LA",
        "a sex addict",
        "an alcoholic",
        "Stalin",
        "a giant elephant",
        "a cute cat",
        "a cute dog",
        "a wild rabbit",
    ]:
        for question in questions_expanded:
            data.append(
                {
                    **question,
                    "persona": persona,
                    "prompt": prompt.format(
                        a=question["a"],
                        persona=persona,
                        b=question["b"],
                        question=question["question"],
                    ),
                }
            )


@async_wrap
def get_answer_async(row):
    return get_answer(row)


def get_answer(row):
    try:
        r = oai.query_openai_chat_conversation(
            [
                {
                    "role": "user",
                    "content": row["prompt"],
                },
            ],
            request_timeout=30,
        )
        logging.info(f"@{row['persona']} {row['question']} {r['response']}")
        row["json_response"] = r["response"].replace("\n", "\\n")
    except Exception as e:
        logging.error(e)
    return row


data = parallel_v2(data, get_answer_async, concurrency=10)
now = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")
pandas.DataFrame(data)[
    ["persona", "question", "complimentary", "a", "b", "json_response"]
].to_csv(
    f"{os.environ['HOME']}/github.com/loicbourgois/downtowhat/data_builder/archive/answers_{now}.csv",
    index=False,
)
