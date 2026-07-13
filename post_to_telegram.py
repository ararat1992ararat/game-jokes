import json
import os
import random
import urllib.parse
import urllib.request

CHANNEL = "@anekdoty_daily"
JOKES_PER_POST = 5
SEPARATOR = "\n\n➖➖➖\n\n"
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


def pick_jokes(all_jokes: list[str], posted: list[str], count: int) -> tuple[list[str], list[str]]:
    posted_set = set(posted)
    unposted = [j for j in all_jokes if j not in posted_set]
    picked: list[str] = []

    while len(picked) < count:
        if not unposted:
            posted = []
            unposted = [j for j in all_jokes if j not in picked]
            if not unposted:
                break
        joke = random.choice(unposted)
        unposted.remove(joke)
        picked.append(joke)

    return picked, posted + picked


def send_message(text: str) -> None:
    data = urllib.parse.urlencode({"chat_id": CHANNEL, "text": text}).encode()
    req = urllib.request.Request(API_URL, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(resp.read().decode("utf-8"))


def main() -> None:
    all_jokes = load_jokes()
    posted = load_posted()

    picked, posted = pick_jokes(all_jokes, posted, JOKES_PER_POST)
    if not picked:
        print("Нет анекдотов для публикации")
        return

    message = SEPARATOR.join(picked) + SIGNATURE
    send_message(message)

    save_posted(posted)
    print(f"Опубликовано {len(picked)} анекдотов")


if __name__ == "__main__":
    main()
