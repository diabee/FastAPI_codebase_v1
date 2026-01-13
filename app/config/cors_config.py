import os
from fastapi.middleware.cors import CORSMiddleware


class CorsConfig:
    def __init__(self):
        pass

    @classmethod
    def init_cors(cls, app=None):
        origins = os.getenv("CORS_ORIGINS", "*").split(",")
        methods = os.getenv("CORS_METHODS", "*").split(",")
        headers = os.getenv("CORS_HEADERS", "*").split(",")
        credentials = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=methods,
            allow_headers=headers,
            allow_credentials=credentials,
        )

