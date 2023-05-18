from api.routes.routes import router as grades


def import_routers(app):
    app.include_router(grades)