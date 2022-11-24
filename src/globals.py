import os
import sys
from distutils.util import strtobool
from pathlib import Path

import supervisely as sly

root_source_path = str(Path(sys.argv[0]).parents[2])
sly.logger.info(f"Root source directory: {root_source_path}")
sys.path.append(root_source_path)

# only for debug
# from dotenv import load_dotenv
# load_dotenv(os.path.expanduser("~/supervisely.env"))
# load_dotenv("local.env")

api = sly.Api.from_env()

TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
PROJECT_ID = sly.env.project_id()
DATASET_ID = sly.env.dataset_id()

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
