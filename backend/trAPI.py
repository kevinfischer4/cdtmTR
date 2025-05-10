#!/usr/bin/env python3
"""
Keeps a background heartbeat and reader running in parallel.
Requires: pip install websockets
"""

import asyncio
import json
import signal
import websockets

URI = "wss://api.traderepublic.com"
HEARTBEAT_INTERVAL = 30  # seconds

async def subscribe(ws, channel: int, payload: dict):
    await ws.send(f"sub {channel} {json.dumps(payload)}")

async def heartbeat(ws):
    try:
        while True:
            await asyncio.sleep(HEARTBEAT_INTERVAL)
            await ws.ping()                # keep the connection alive
    except asyncio.CancelledError:
        return

async def reader(ws):
    async for message in ws:            # will yield every incoming frame
        print("<", message)

async def main():
    # allow Ctrl+C to cancel everything
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)

    async with websockets.connect(URI, ping_interval=None) as ws:
        # 1) Negotiate heartbeat interval
        await ws.send(f"connect {HEARTBEAT_INTERVAL}")
        print("<", await ws.recv())

        # 2) Subscribe both channels
        await subscribe(ws, 2, {"type": "ticker",     "id": "DE000BASF111.LSX"})

        # 3) Run heartbeat + reader concurrently until SIGINT
        hb_task = asyncio.create_task(heartbeat(ws))
        read_task = asyncio.create_task(reader(ws))
        await stop                             # wait for Ctrl+C
        hb_task.cancel()
        read_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
