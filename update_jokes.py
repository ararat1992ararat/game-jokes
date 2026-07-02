import json
import random
from datetime import date

# Сколько анекдотов показывать в день
JOKES_PER_DAY = 5

with open("all_jokes.json", "r", encoding="utf-8") as f:
    all_jokes = json.load(f)["jokes"]

today = date.today().isoformat()

# Используем дату как seed, чтобы каждый день была
# стабильная, но новая подборка анекдотов
rng = random.Random(today)
selected = rng.sample(all_jokes, min(JOKES_PER_DAY, len(all_jokes)))

result = {
    "date": today,
    "jokes": selected
}

with open("jokes.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Обновлено на {today}: {len(selected)} анекдотов")
