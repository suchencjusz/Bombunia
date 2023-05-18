import uvicorn

from api.config import import_routers
from api.database.db import DB
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def get_app() -> FastAPI:
    _app = FastAPI()
    origins = ["*"]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    import_routers(_app)

    return _app


app = get_app()


if __name__ == "__main__":

    # host = env.get("HOST", "8080")
    # port = int(env.get("PORT", "8080"))

    host = "localhost"
    port = "8080"

    is_reload = False
    # is_reload = strtobool(env.get("RELOAD", "False"))

    # uvicorn.run("__main__:app", host=host, port=port, reload=is_reload)
    uvicorn.run("__main__:app", host="127.0.0.1", port=8080)
