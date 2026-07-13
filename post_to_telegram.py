import json
import os
import random
import urllib.parse
import urllib.request

CHANNEL = "@anekdoty_daily"
SIGNATURE = "\n\n📌 Анекдоты каждый день — подпишись!\nhttps://t.me/+AvQyxbNRhntkZDBi"
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
POSTED_PATH = "posted_jokes.json"


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


def send_message(text: str) -> None:
    data = urllib.parse.urlencode({"chat_id": CHANNEL, "text": text}).encode()
    req = urllib.request.Request(API_URL, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(resp.read().decode("utf-8"))


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
    send_message(joke + SIGNATURE)

    posted.append(joke)
    save_posted(posted)
    print("Опубликовано:", joke[:60])


if __name__ == "__main__":
    main()
