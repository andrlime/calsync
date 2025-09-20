import arrow

import calsync.core.event as event
from calsync.util.logger import create_logger

logger = create_logger()


class EventStore_:
    def __init__(self) -> None:
        self.store: dict[str, list[event.T]] = {}

    def get_date_string(self, time: arrow.Arrow) -> str:
        return time.format("YY-MMDD-dddd")

    def create_bucket(self, time: arrow.Arrow) -> str:
        key = self.get_date_string(time)
        if key not in self.store:
            self.store[key] = []
        return key

    def add_event(self, e: event.T) -> bool:
        key = self.create_bucket(e.rawday)
        self.store[key].append(e)
        return True

    def sort_buckets(self) -> bool:
        for bucket in self.store.values():
            bucket.sort(key=lambda e: e.starttime)
        return True

    def get(self) -> dict[str, list[event.T]]:
        return self.store


class BucketEvents:
    def __init__(self, events: list[event.T], days: list[arrow.Arrow]) -> None:
        logger.info(
            f"Initializing BucketEvents with {len(events)} events across {len(days)} days"
        )
        self.store = EventStore_()
        [self.store.create_bucket(d) for d in days]
        [self.store.add_event(e) for e in events]
        self.store.sort_buckets()
        logger.info("BucketEvents initialization completed")

    def filt(self) -> dict[str, list[event.T]]:
        buckets = self.store.get()
        logger.info(f"Event bucketing completed: {len(buckets)} day buckets created")
        return buckets
