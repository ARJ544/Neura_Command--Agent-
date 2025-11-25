from core.runner import run_loop
import asyncio
import sys

if __name__ == "__main__":
    try:
        asyncio.run(run_loop())
    except (KeyboardInterrupt, EOFError, asyncio.CancelledError):
        print("\nExiting cleanly...")
        sys.exit(0)
