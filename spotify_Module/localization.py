import json

def load_Vocabluary():
    with open("locales/spotify/english.json", encoding="utf-8-sig") as json_English, open("locales/spotify/russian.json", encoding="utf-8-sig") as json_Russian:
        english_Language = json.load(json_English)
        russian_Language = json.load(json_Russian)

        language_Vocabluary = {
            "ENG":english_Language,
            "RUS":russian_Language,
        }

        return language_Vocabluary