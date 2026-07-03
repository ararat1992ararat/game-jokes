import json

with open("all_jokes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fixed_jokes = [joke.replace("\\n", "\n") for joke in data["jokes"]]

with open("all_jokes.json", "w", encoding="utf-8") as f:
    json.dump({"jokes": fixed_jokes}, f, ensure_ascii=False, indent=2)

print(f"Исправлено анекдотов: {len(fixed_jokes)}")
