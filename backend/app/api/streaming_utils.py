import json
import threading
from queue import Queue
from typing import Any, Callable, Iterator

from fastapi.responses import StreamingResponse

from app.domain.streaming import StreamSink

CommandFn = Callable[[StreamSink], Any]


def stream_command(
    command: CommandFn,
) -> StreamingResponse:
    """
    Runs a command that may emit solution text via a stream sink
    and returns an SSE StreamingResponse.
    """
    queue: Queue[str | None] = Queue()

    def stream_sink(delta: str | None) -> None:
        queue.put(delta)

    def sse(event: str, payload: dict[str, Any]) -> str:
        return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"

    def sse_text(event: str, text: str) -> str:
        return sse(event, {"text": text})

    def event_stream() -> Iterator[str]:
        try:
            # Run the command (engine decides if/when streaming happens)
            def run():
                try:
                    command(stream_sink)
                finally:
                    stream_sink(None)

            # 🔥 Run command in background
            thread = threading.Thread(target=run, daemon=True)
            thread.start()

            # 🔥 Yield while command is running
            while True:
                chunk = queue.get()
                if chunk is None:
                    break
                yield sse_text("chunk", chunk)

            yield sse("done", {"ok": True})

        except Exception as e:
            yield sse_text("error", str(e))
            yield sse("done", {"ok": False})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # VERY IMPORTANT (nginx, uvicorn)
        },
    )
