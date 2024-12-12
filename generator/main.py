from ..utils import logging
logging.info("start")
from ..utils.files import write_force
from ..utils.files import read
from ..utils.files import file_exists
from ..utils.files import list_all_files
from ..utils.math import cosine_similarity
import hashlib
import uuid
import os
import requests
import json
from uuid import UUID
def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
content = ["grouping\tpriority\thash\tlabel"]
options = read("/root/github.com/loicbourgois/downtowhat/generator/options.txt").split("\n")
option_ok = {}
priority = 1
group = 0
logging.info("building options")
for option_list in options:
    group += 1
    for option in option_list.split("|"):
        option = option.lower().strip()
        if len(option) < 2:
            continue
        if "\t" in option:
            logging(f"invalid: {option}")
            continue
        if option[0] == "#":
            continue
        m = hashlib.sha1()
        m.update(option.encode('utf-8'))
        h = m.hexdigest()
        content.append(f"{group}\t{priority}\t{h}\t{option}")
        priority += 1
        embedding_path = f"/root/github.com/loicbourgois/downtowhat/generated/embedding/{h}.json"
        if not file_exists(embedding_path):
            r = requests.post(
                "https://api.openai.com/v1/embeddings", 
                headers={
                    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                    "Content-Type": "application/json",
                },
                json={
                    "input": option,
                    "model": "text-embedding-3-small"
                }
            )
            write_force(
                embedding_path,
                json.dumps({
                    "status_code": r.status_code,
                    "response": r.json(),
                    "hash": h,
                    "option": option,
                }, indent=2)
            )
        option_ok[h] = h
write_force(
    "/root/github.com/loicbourgois/downtowhat/generated/options.tsv",
    "\n".join(content)
)
logging.info("building cosine_similarity")
files = list_all_files("/root/github.com/loicbourgois/downtowhat/generated/embedding", "*")
content = ["a\tb\tcosine_similarity"]
for path_a in files:
    aj = json.loads(read(path_a))
    a = aj['response']['data'][0]['embedding']
    ah = aj['hash']
    for path_b in files:
        if path_a == path_b:
            continue
        bj = json.loads(read(path_b))
        b = json.loads(read(path_b))['response']['data'][0]['embedding']
        bh = bj['hash']
        if option_ok.get(ah) and option_ok.get(bh):
            x = cosine_similarity(a,b)
            content.append(f"{ah}\t{bh}\t{x}")
write_force(
    "/root/github.com/loicbourgois/downtowhat/generated/cosine_similarity.tsv",
    "\n".join(content)
)
