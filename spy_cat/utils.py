import os
import requests
from rest_framework.exceptions import ValidationError


CAT_API_KEY = os.getenv("CAT_API_KEY")
URL = "https://api.thecatapi.com/v1/breeds"


def validate_breed(breed):
    headers = {"x-api-key": CAT_API_KEY} if CAT_API_KEY else {}
    response = requests.get(url=URL, headers=headers)
    if response.status_code != 200:
        raise ValidationError(
            "Could not validate breed. Please try again later."
        )
    breeds = [item['name'].lower() for item in response.json()]

    if breed.lower() not in breeds:
        raise ValidationError(f"{breed} is not a recognized breed.")
