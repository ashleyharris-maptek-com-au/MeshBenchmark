import os
import tempfile
import json
import hashlib
import datetime
import time
import random
class CacheLayer:
    def __init__(self, configAndSettingsHash, aiEngineHook):
        self.hash = configAndSettingsHash
        self.aiEngineHook = aiEngineHook
        self.temp_dir = tempfile.gettempdir()

    def AIHook(self, prompt: str, structure: dict | None) -> dict | str:
        h = (hashlib.sha256(prompt.strip().encode()).hexdigest(),
             hashlib.sha256(str(structure).encode()).hexdigest(),
             self.hash,
             datetime.datetime.now().strftime("%b %Y"))

        h = hashlib.sha256(str(h).encode()).hexdigest()

        cache_file = os.path.join(self.temp_dir, "cache_" + str(h) + ".txt")

        if os.path.exists(cache_file):
          try:
            with open(cache_file, "r",encoding="utf-8") as f:
                cachedJson = json.load(f)
                if len(cachedJson) > 0:
                  return cachedJson
          except Exception as e:
            print("Failed to read cache file: " + cache_file + " - " + str(e))
            try:
              os.unlink(cache_file)
            except:
              pass

        print("API Call: " + prompt[:100].replace("\n", " ") + "...")

        print("Started at " + str(datetime.datetime.now()))
        result = self.aiEngineHook(prompt, structure)

        if not result:
          print("Empty result or Error 500, pausing and then retrying in a few minutes...")
          time.sleep(60 + random.randint(0, 120))
          result = self.aiEngineHook(prompt, structure)

        print("Finished at " + str(datetime.datetime.now()))

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f)
        return result
