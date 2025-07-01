# main.py

# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client
import importlib
import os

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [
        f[:-3] for f in os.listdir(plugin_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            if hasattr(module, f"run_{plugin}_plugin"):
                print(f"Running {plugin} plugin...")
                await getattr(module, f"run_{plugin}_plugin")()
        except Exception as e:
            print(f"⚠️ Error loading plugin '{plugin}': {e}")

async def main():
    print("Starting clients ...")
    await load_and_run_plugins()
    await asyncio.Event().wait()  # Keeps the app running indefinitely

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
