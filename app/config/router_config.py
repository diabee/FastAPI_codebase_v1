from app.example.controller.example_controller import example_router


class RoutesConfig:
    def __init__(self, app):
        app.include_router(example_router)
