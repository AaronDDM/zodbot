import dataclasses
import json
import os
import time

class Cache():
    def __init__(self, cache_dir, cache_name, cache_time):
        self.cache_dir = cache_dir
        self.cache_name = cache_name
        self.cache_time = cache_time
        self.cache = {}
        self.load_cache()

        # Create the cache directory if it does not exist
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def load_cache(self):
        try:
            with open(os.path.join(self.cache_dir, self.cache_name), 'r') as f:
                self.cache = json.load(f)
        except:
            pass

    def save_cache(self):
        with open(os.path.join(self.cache_dir, self.cache_name), 'w') as f:
            json.dump(self.cache, f)

    def get(self, key):
        if key in self.cache:
            if time.time() - self.cache[key]['time'] < self.cache_time:
                return self.cache[key]['value']
            else:
                del self.cache[key]
                self.save_cache()
        return None

    def set(self, key, value):
        if dataclasses.is_dataclass(value):
            v = value.asdict()
        else:
            v = value

        self.cache[key] = {'value': v, 'time': time.time()}
        self.save_cache()