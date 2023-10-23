import g4f
import os

PROXY = 'http://proxy.server:3128'
CLOUD = os.getenv('CLOUD')
g4f.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking



def gpt4(input: str)->str:
    return _gpt(input, g4f.models.gpt_4)



def _gpt(input: str, mdl)->str:
    if CLOUD == "PYTHONANYWHERE"
        return g4f.ChatCompletion.create(
                model=mdl,
                provider=g4f.Provider.Aichat,
                messages=[{"role": "user", "content": input}],
                proxy=PROXY
            )
    return g4f.ChatCompletion.create(
                model=mdl,
                provider=g4f.Provider.Aichat,
                messages=[{"role": "user", "content": input}],
            )