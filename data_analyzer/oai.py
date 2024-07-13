"""Usage:
oai = Openai(
    api_key=os.environ['OPENAI_API_KEY'],
    organization=os.environ['OPENAI_ORGANIZATION'],
)
r1 = oai.query_openai_chat_conversation(
    [
        {"role": "user", "content": "Hey"},
    ],
)
r2 = oai.query_openai_chat_conversation(
    [
        {"role": "user", "content": "Hey"},
        {"role": "assistant", "content": r1['response']},
        {"role": "assistant", "content": "How are you ?"},
    ],
)
"""

import datetime
import time
from random import random
import uuid
import json
import openai
import pandas
from .log import (
    logging,
)
from .parallel_v2 import (
    async_wrap,
)


class Openai:
    def __init__(self, verbose=False, api_key=None, organization=None) -> None:
        self.api_key = api_key
        self.organization = organization
        self.verbose = verbose
        self.history = pandas.DataFrame()
        self.pipeline_id = uuid.uuid4()
        self.pipeline_start_time = datetime.datetime.utcnow()
        self.bq_table = ""
        self.models = {
            "gpt-3.5-turbo": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "unit_cost": {
                    "prompt": 0.002 / 1000,
                    "completion": 0.002 / 1000,
                },
            },
            "gpt-4": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "unit_cost": {
                    "prompt": 0.03 / 1000,
                    "completion": 0.06 / 1000,
                },
            },
        }

    def total_cost(self):
        c = 0
        for _, v in self.models.items():
            c += v["unit_cost"]["prompt"] * v["prompt_tokens"]
            c += v["unit_cost"]["completion"] * v["completion_tokens"]
        return c

    def unload_history(self):
        if self.history.shape[0] > 0:

            def apply(row):
                row["messages"] = json.dumps(row["messages"])
                return row

            self.history = self.history.apply(apply, axis=1)
            self.history.astype(
                {
                    "messages": str,
                }
            )
            # df_to_bq(self.history, 'poc.gpt_v3')
            self.history = pandas.DataFrame()

    @async_wrap
    def query_openai_chat_async(self, prompt, model="gpt-3.5-turbo"):
        return self.query_openai_chat(prompt, model)

    def query_openai_chat(self, prompt, model="gpt-3.5-turbo", max_retry=3, backoff=2):
        return {
            **self.query_openai_chat_conversation(
                [
                    {"role": "user", "content": prompt},
                ],
                model,
                max_retry,
                backoff,
            ),
            "prompt": prompt,
        }

    @async_wrap
    def query_openai_chat_conversation_async(
        self,
        messages,
        model="gpt-3.5-turbo",
        max_retry=3,
        backoff=2,
        request_timeout=5 * 60,
    ):
        return self.query_openai_chat_conversation(
            messages, model, max_retry, backoff, request_timeout
        )

    def query_openai_chat_conversation(
        self,
        messages,
        model="gpt-3.5-turbo",
        max_retry=3,
        backoff=2,
        request_timeout=5 * 60,
    ):
        if max_retry < 0:
            logging.error("ERROR - query_openai_chat_conversation")
            return {
                "messages": messages,
                "response": "",
                "total_tokens": 0,
                "model": model,
            }
        if len(messages) <= 0:
            return {
                "messages": messages,
                "response": "",
                "total_tokens": 0,
                "model": model,
            }
        try:
            r = openai.ChatCompletion.create(
                api_key=self.api_key,
                organization=self.organization,
                model=model,
                messages=messages,
                request_timeout=request_timeout,
            )
            response = r["choices"][0]["message"]["content"]
            if self.verbose:
                logging.info(
                    "\n".join(
                        [f"# {x['role']}\n{str(x['content'])}" for x in messages]
                        + [f"# assistant\n{response}"]
                    )
                )
            self.models[model]["total_tokens"] += r["usage"]["total_tokens"]
            self.models[model]["completion_tokens"] += r["usage"]["completion_tokens"]
            self.models[model]["prompt_tokens"] += r["usage"]["prompt_tokens"]
            r = {
                "messages": messages,
                "response": response,
                "prompt_tokens": int(r["usage"]["prompt_tokens"]),
                "completion_tokens": int(r["usage"]["completion_tokens"]),
                "total_tokens": int(r["usage"]["total_tokens"]),
                "model": model,
                "pipeline_id": str(self.pipeline_id),
                "pipeline_start_time": (self.pipeline_start_time),
                "created_at": (datetime.datetime.utcnow()),
            }
            self.history = pandas.concat([self.history, pandas.DataFrame([r])])
            return r
        except Exception as e:
            logging.warning(e)
            time.sleep(random() * backoff)
            return self.query_openai_chat_conversation(
                messages, model, max_retry - 1, backoff * 2
            )
