import os
from distutils.util import strtobool

import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()

TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
PROJECT_ID = sly.env.project_id()
DATASET_ID = sly.env.dataset_id(raise_not_found=False)

KEEP_ANNS = bool(strtobool(os.getenv("modal.state.keepAnns")))
PROJECT_NAME = os.environ["modal.state.projectName"]

SUPPORTED_GEOMETRY_TYPES = [
    sly.AnyGeometry,
    sly.Bitmap,
    sly.Polygon,
    sly.Polyline,
    sly.Rectangle,
]

app = sly.Application()
