import os  # Importa os para manejar correctamente los paths
import glob
import json
from typing import Dict

from fastapi import Request

from infrastructure.commons.constants.locales import ES_LOCALE, EN_LOCALE
from infrastructure.commons.enums.error_message import ErrorMessageKey

languages = {}


def load_locales() -> Dict:
    language_list = glob.glob("locales/*.json")
    for lang in language_list:
        filename = os.path.basename(lang)  # Obtén solo el nombre del archivo
        lang_code = filename.split('.')[0]  # Divide por punto para obtener el código de idioma

        with open(lang, 'r', encoding='utf8') as file:
            languages[lang_code] = json.load(file)
    return languages


def translate_message(request: Request, key: ErrorMessageKey):
    locale = get_locale(request)
    return languages[locale][key.value]


def get_locale(request: Request):
    locale = request.headers.get("Locale", ES_LOCALE)
    if locale and "en" in locale:
        return EN_LOCALE
    return ES_LOCALE
