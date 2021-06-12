from utils.app import App


def get_asgi_application():
    app = App()
    # TODO: config exception handlers event handlers and middlewares

    return app
