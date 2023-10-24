import g4f
import os


CLOUD = os.getenv('CLOUD')
g4f.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking



def gpt4(input: str)->str:
    if CLOUD == "PYTHONANYWHERE":
        return g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                provider=g4f.Provider.Bing,
                messages=[{"role": "user", "content": input}],
                proxy=os.getenv('http_proxy')
            )
    return g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": input}],
            )


def bard(input: str)->str:
    if CLOUD == "PYTHONANYWHERE":
        return g4f.ChatCompletion.create(
                model=g4f.models.palm,
                provider=g4f.Provider.Bard,
                messages=[{"role": "user", "content": input}],
                proxy=os.getenv('http_proxy')
            )
    return g4f.ChatCompletion.create(
                model=g4f.models.palm,
                provider=g4f.Provider.Bard,
                messages=[{"role": "user", "content": input}],
            )