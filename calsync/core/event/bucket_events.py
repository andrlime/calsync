from collections import defaultdict

import calsync.core.event as event
from calsync.util.logger import create_logger

logger = create_logger()


class BucketEvents:
    def __init__(self, events: list[event.T]):
        self.store = defaultdict(list)
        for e in events:
            self.store[f"{e.year}-{e.day}-{e.month}"].append(e)
        for bucket in self.store.values():
            bucket.sort(key=lambda e: e.starttime)

    def filt(self) -> dict[str, list[event.T]]:
        logger.info("Bucket events ok")
        return self.store
