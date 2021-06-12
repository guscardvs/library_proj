from core.settings import BASE_DIR
from database.common.entity import Entity
from database.common.model_finder import ModelFinder


def get_metadata():

    DATABASE_FOLDER = BASE_DIR / "database"

    model_finder = ModelFinder(DATABASE_FOLDER / "models", DATABASE_FOLDER)
    model_finder.find()
    return Entity.metadata
