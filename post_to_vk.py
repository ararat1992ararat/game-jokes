import json
import os
import random
import urllib.parse
import urllib.request

GROUP_ID = os.environ["VK_GROUP_ID"]
ACCESS_TOKEN = os.environ["VK_ACCESS_TOKEN"]
SIGNATURE = "\n\n📌 Анекдоты каждый день — подпишись!\nhttps://t.me/+AvQyxbNRhntkZDBi"
API_URL = "https://api.vk.com/method/wall.post"
API_VERSION = "5.199"
POSTED_PATH = "posted_jokes_vk.json"


def load_jokes() -> list[str]:
    with open("all_jokes.json", "r", encoding="utf-8") as f:
        return json.load(f)["jokes"]


def load_posted() -> list[str]:
    if not os.path.exists(POSTED_PATH):
        return []
    with open(POSTED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["posted"]


def save_posted(posted: list[str]) -> None:
    with open(POSTED_PATH, "w", encoding="utf-8") as f:
        json.dump({"posted": posted}, f, ensure_ascii=False, indent=2)


def post_to_wall(text: str) -> None:
    params = {
        "owner_id": f"-{GROUP_ID}",
        "message": text,
        "from_group": 1,
        "access_token": ACCESS_TOKEN,
        "v": API_VERSION,
    }
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(API_URL, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = resp.read().decode("utf-8")
        print(result)
        if '"error"' in result:
            raise RuntimeError(f"VK API error: {result}")


def main() -> None:
    all_jokes = load_jokes()
    posted = load_posted()
    posted_set = set(posted)

    unposted = [j for j in all_jokes if j not in posted_set]
    if not unposted:
        posted = []
        unposted = all_jokes

    if not unposted:
        print("Нет анекдотов для публикации")
        return

    joke = random.choice(unposted)
    post_to_wall(joke + SIGNATURE)

    posted.append(joke)
    save_posted(posted)
    print("Опубликовано в ВК:", joke[:60])


if __name__ == "__main__":
    main()
