import arrow

import calsync.core.event as event
from calsync.util.logger import create_logger

logger = create_logger()


class BucketEvents:
    def __init__(self, events: list[event.T], days: list[arrow.Arrow]):
        self.store: dict[str, list[event.T]] = {}
        for d in days:
            self.store[d.format("YY-MMDD-dddd")] = []
        for e in events:
            key = e.rawday.format("YY-MMDD-dddd")
            if key not in self.store:
                self.store[key] = []
            self.store[key].append(e)
        for bucket in self.store.values():
            bucket.sort(key=lambda e: e.starttime)

    def filt(self) -> dict[str, list[event.T]]:
        logger.info("Bucket events ok")
        return self.store
