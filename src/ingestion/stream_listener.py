import asyncio
import json
import logging
from typing import AsyncGenerator, Callable, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ApexIngestionStream")

class StreamListener:
    """Listens to live CI/CD webhook streams, log files, and real-time event feeds."""
    
    def __init__(self, buffer_size: int = 100):
        self.buffer_size = buffer_size
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)

    async def push_event(self, source, event_data: Dict[str, Any] = None):
        """Pushes an incoming webhook or log event into the real-time buffer.

        Accepts both call formats:
          push_event("github_webhook", {"action": "push"})
          push_event({"github_webhook": {"action": "push"}})
        Both normalize to {"source": <source>, "data": <event_data>}.
        """
        if event_data is None and isinstance(source, dict):
            if "source" in source and "data" in source:
                payload = {"source": source["source"], "data": source["data"]}
            elif len(source) == 1:
                src, data = next(iter(source.items()))
                payload = {"source": src, "data": data}
            else:
                payload = {"source": "unknown", "data": source}
        else:
            payload = {"source": source, "data": event_data}
        if self._queue.full():
            logger.warning("Stream buffer full. Evicting oldest log event.")
            self._queue.get_nowait()
        await self._queue.put(payload)

    async def tail_log_file(self, file_path: str, poll_interval: float = 0.5) -> AsyncGenerator[str, None]:
        """Asynchronously tails a local log file or CI output stream for real-time triage."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                f.seek(0, 2)  # Seek to end of file
                while True:
                    line = f.readline()
                    if line:
                        yield line.strip()
                    else:
                        await asyncio.sleep(poll_interval)
        except Exception as e:
            logger.error(f"Error tailing log file {file_path}: {e}")

    async def stream_generator(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Yields streaming event chunks to Tier 1 Ingestion Context Engine."""
        while True:
            event = await self._queue.get()
            yield event
            self._queue.task_done()
