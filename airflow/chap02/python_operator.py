import pathlib


def _get_pictures():
    pathlib.Path("./tmp/images").mkdir(parents=True, exist_ok=True)
