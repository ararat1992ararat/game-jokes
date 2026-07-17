from __future__ import annotations

import json
import re
import urllib.request
from datetime import date

NEW_JOKES_TO_FETCH = 10
API_URL = "http://rzhunemogu.ru/RandJSON.aspx?CType=1"

CYRILLIC_RE = re.compile(r"[а-яА-ЯёЁ]")
LETTER_RE = re.compile(r"[a-zA-Zа-яА-ЯёЁ]")


## rzhunemogu.ru's own database has leaked at least one raw SQL injection
## probe (a WAITFOR/DELAY payload) through this API and into our joke pool -
## reject anything that isn't mostly Cyrillic text before it gets accepted.
def is_junk(text: str) -> bool:
    letters = LETTER_RE.findall(text)
    if not letters:
        return True
    return (len(CYRILLIC_RE.findall(text)) / len(letters)) < 0.5


def fetch_one_joke() -> str | None:
    try:
        req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("cp1251", errors="ignore")
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None

    fixed = raw.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")
    match = re.search(r'"content"\s*:\s*"(.*)"\s*}', fixed, re.DOTALL)
    if not match:
        return None

    text = match.group(1)
    text = text.replace('\\"', '"')
    text = text.replace("\\n", "\n")  # превращаем текстовые \n в настоящий перенос строки
    return text.strip() if text.strip() else None


def load_all_jokes() -> list[str]:
    with open("all_jokes.json", "r", encoding="utf-8") as f:
        return json.load(f)["jokes"]


def save_all_jokes(jokes: list[str]) -> None:
    with open("all_jokes.json", "w", encoding="utf-8") as f:
        json.dump({"jokes": jokes}, f, ensure_ascii=False, indent=2)


def main():
    all_jokes = load_all_jokes()
    existing = set(all_jokes)

    fetched_count = 0
    for _ in range(NEW_JOKES_TO_FETCH):
        joke = fetch_one_joke()
        if joke and joke not in existing and 10 < len(joke) < 1000 and not is_junk(joke):
            all_jokes.append(joke)
            existing.add(joke)
            fetched_count += 1

    print(f"Добавлено новых анекдотов: {fetched_count}")
    save_all_jokes(all_jokes)

    today = date.today().isoformat()
    with open("jokes.json", "w", encoding="utf-8") as f:
        json.dump({"date": today, "jokes": all_jokes}, f, ensure_ascii=False, indent=2)

    print(f"jokes.json обновлён на {today}: всего анекдотов в базе — {len(all_jokes)}")


if __name__ == "__main__":
    main()
