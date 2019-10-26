from brewtils import system, parameter, Plugin


@system
class HelloClient(object):

    @parameter(key="message", type="String", default="Hello, World!")
    def say_hello(self, message):
        print(message)
        return message


if __name__ == "__main__":
    client = HelloClient()

    plugin = Plugin(
        client,
        name="hello-world",
        version="0.0.1.dev0",
        bg_host='localhost',
        bg_port=2337,
        ssl_enabled=False,
    )
    plugin.run()