from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import re
from dotenv import load_dotenv
import os

import requests

manual = """
Use GET /notes to list notes
example response body:
    [
       {
          "id": "ehgwc6a8RXSmcSaRwIQ2jw",
          "title": "Personal note title",
          "tags": ["personal", "test"],
          "createdAt": 1643270371245,
          "publishType": "view",
          "publishedAt": null,
          "permalink": null,
          "shortId": "SysJb0yAY",
          "lastChangedAt": 1643270452413,
          "lastChangeUser": {
              "name": "James",
              "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
              "biography": null,
              "userPath": "AMQ36J15QgCZf46ThEFadg"
          },
          "userPath": "AMQ36J15QgCZf46ThEFadg",
          "teamPath": null,
          "readPermission": "guest",
          "writePermission": "signed_in",
          "publishLink": "https://hackmd.io/@username/permalink"
        }
     ]
Use GET /notes/<noteId> to get note content
example response body:
    {
        "id": "ehgwc6a8RXSmcSaRwIQ2jw",
        "title": "Personal note title",
        "tags": [
            "Personal",
            "test"
        ],
        "createdAt": 1643270371245,
        "publishType": "view",
        "publishedAt": null,
        "permalink": null,
        "shortId": "SysJb0yAY",
        "content": "# Personal note title\n###### tags: `Personal` `test`",
        "lastChangedAt": 1644461594806,
        "lastChangeUser": {
            "name": "James",
            "photo": "https://avatars.githubusercontent.com/u/26138990?s=96",
            "biography": null,
            "userPath": "AMQ36J15QgCZf46ThEFadg"
        },
        "userPath": "AMQ36J15QgCZf46ThEFadg",
        "teamPath": null,
        "readPermission": "guest",
        "writePermission": "signed_in",
        "publishLink": "https://hackmd.io/@username/permalink"                
    }
Use POST /notes to create a new note
example request body:
{
    "title": "New note",
    "content": "",
    "readPermission": "owner",
    "writePermission": "owner",
    "commentPermission": "everyone"
}
Use PATCH /notes/:noteId to update a note
example request body:
  {
    "content": "# Updated personal note",
    "readPermission": "signed_in",
    "writePermission": "owner",
    "permalink": "note-permalink"
  }
"""


# 計算檔案的哈希值
def calculate_hash(content):
    hasher = hashlib.sha3_256()
    hasher.update(content.encode("utf-8"))
    return hasher.hexdigest()


# 讀取已保存的哈希值
def load_hashes(hash_file):
    try:
        with open(hash_file, "r") as f:
            return json.load(f)
    except:
        pass
    return {}


# 保存哈希值
def save_hashes(hash_file, hashes):
    with open(hash_file, "w") as f:
        json.dump(hashes, f, indent=4)


hash_file = "file_hashes.json"
hashes = load_hashes(hash_file)


load_dotenv()
token = os.getenv("TOKEN")
url = "https://api.hackmd.io/v1"

# 設置請求頭
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for root, dirs, files in os.walk("."):
        for filename in files:
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            file_hash = calculate_hash(content)
            if hashes.get(filepath) == file_hash:
                print(f"No changes in file: {filepath}")
                continue
            pattern = r"<!-- HackMD ID: *([^ ]*) *-->"
            match = re.search(pattern, content)
            if match:
                print(f"Updating note: {filepath}")
                # 獲取 HackMD ID
                hackmd_id = match.group(1)
                content = re.sub(pattern+r" *\n?", "", content, count=1)
                # print(content)
                # 構建請求數據
                data = {"content": content}
                # 發送 PATCH 請求更新筆記
                futures.append(
                    executor.submit(
                        lambda filepath, file_hash: (
                            filepath,
                            file_hash,
                            requests.patch(
                                f"{url}/notes/{hackmd_id}", headers=headers, json=data
                            ),
                        ),
                        filepath,
                        file_hash,
                    )
                )
    for future in as_completed(futures):
        filepath, file_hash, response = future.result()
        if response.status_code == 202:
            print(f"Successfully updated note: {filepath}")
            print(f"body: \"{response.text}\"")
            hashes[filepath] = file_hash
        else:
            print(
                f"Failed to update note: {filepath}, Status Code: {response.status_code}, Response: {response.text}"
            )
save_hashes(hash_file, hashes)
