from brewtils import system, parameter, Plugin
from CanvasApi import CanvasApi

if __name__ == "__main__":
    client = CanvasApi()

    plugin = Plugin(
        client,
        name="Canvas Debugger",
        version="1.0",
        bg_host='localhost',
        bg_port=2337,
        ssl_enabled=False,
    )
    plugin.run()