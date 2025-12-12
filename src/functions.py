import math
from typing import List

import cv2
import numpy as np
import supervisely as sly

from src.globals import (
    DST_GEOMETRY,
    KEEP_ANNS,
    PROJECT_ID,
    PROJECT_NAME,
    SUPPORTED_GEOMETRY_TYPES,
    WORKSPACE_ID,
)


def create_project(api: sly.Api):
    src_project_meta = sly.ProjectMeta.from_json(
        data=api.project.get_meta(id=PROJECT_ID, with_settings=True)
    )
    if DST_GEOMETRY == sly.OrientedBBox:
        ro_bbox_obj_classes = [
            sly.ObjClass(
                name=f"{obj_class.name}_obbox",
                geometry_type=sly.OrientedBBox,
                color=obj_class.color,
            )
            for obj_class in src_project_meta.obj_classes
            if obj_class.geometry_type in SUPPORTED_GEOMETRY_TYPES
        ]
    else:
        ro_bbox_obj_classes = [
            sly.ObjClass(
                name=f"{obj_class.name}_ro_bbox",
                geometry_type=sly.Polygon,
                color=obj_class.color,
            )
            for obj_class in src_project_meta.obj_classes
            if obj_class.geometry_type in SUPPORTED_GEOMETRY_TYPES
        ]

    dst_project_meta = sly.ProjectMeta(
        obj_classes=ro_bbox_obj_classes,
        tag_metas=src_project_meta.tag_metas,
        project_settings=src_project_meta.project_settings,
    )
    if KEEP_ANNS is True:
        dst_project_meta = dst_project_meta.merge(other=src_project_meta)

    dst_project = api.project.create(
        workspace_id=WORKSPACE_ID,
        name=PROJECT_NAME or api.project.get_info_by_id(id=PROJECT_ID).name,
        type=sly.ProjectType.IMAGES,
        change_name_if_conflict=True,
    )
    dst_project_meta = api.project.update_meta(
        id=dst_project.id, meta=dst_project_meta.to_json()
    )
    return dst_project, dst_project_meta, src_project_meta


def copy_ds_images(api: sly.Api, src_ds_id: int, dst_ds_id: int):
    images_infos = api.image.get_list(dataset_id=src_ds_id)
    images_ids = [img_info.id for img_info in images_infos]
    images_names = [img_info.name for img_info in images_infos]
    new_images_infos = api.image.upload_ids(
        dataset_id=dst_ds_id, names=images_names, ids=images_ids
    )
    new_images_ids = [img_info.id for img_info in new_images_infos]
    return new_images_ids


def get_anns_list(api: sly.Api, ds_id: int, project_meta: sly.ProjectMeta):
    image_ids = [img_info.id for img_info in api.image.get_list(ds_id)]
    ann_infos = api.annotation.download_batch(ds_id, image_ids)
    ann_jsons = [ann_info.annotation for ann_info in ann_infos]
    anns = [
        sly.Annotation.from_json(data=ann_json, project_meta=project_meta)
        for ann_json in ann_jsons
    ]
    return anns


def convert_anns(anns: List[sly.Annotation], dst_project_meta: sly.ProjectMeta):
    ro_bbox_anns = []
    for ann in anns:
        ro_bbox_labels = []
        for label in ann.labels:
            if type(label.geometry) not in SUPPORTED_GEOMETRY_TYPES:
                continue
            ro_bbox_label = label_to_ro_bbox(label=label, project_meta=dst_project_meta)
            ro_bbox_labels.append(ro_bbox_label)
        if KEEP_ANNS:
            ro_bbox_anns.append(ann.add_labels(labels=ro_bbox_labels))
        else:
            ro_bbox_anns.append(ann.clone(labels=ro_bbox_labels))
    return ro_bbox_anns


def label_to_ro_bbox(label: sly.Label, project_meta: sly.ProjectMeta):
    suffix = "_obbox" if DST_GEOMETRY == sly.OrientedBBox else "_ro_bbox"
    obj_class_name = f"{label.obj_class.name}{suffix}"
    obj_class = project_meta.get_obj_class(obj_class_name)

    if type(label.geometry) != sly.Polygon:
        geometry = label.geometry.convert(new_geometry=sly.Polygon)[0]
    else:
        geometry = label.geometry

    points = []
    for coord in geometry.exterior:
        coords = np.array([coord.col, coord.row])
        points.append(coords)
    points = np.array(points)

    rect = cv2.minAreaRect(points)
    box = cv2.boxPoints(rect)
    rot_box = np.intp(box)

    coords = [[coord[1], coord[0]] for coord in rot_box]
    if DST_GEOMETRY == sly.OrientedBBox:
        # Extract center, size, and angle from minAreaRect
        (cx, cy), (w, h), angle = rect
        # Normalize so width >= height (landscape orientation)
        if w < h:
            w, h = h, w
            angle += 90
        # Calculate half-dimensions
        half_w, half_h = w / 2, h / 2
        new_geometry = sly.OrientedBBox(
            left=cx - half_w,
            top=cy - half_h,
            right=cx + half_w,
            bottom=cy + half_h,
            angle=math.radians(angle),
        )
    else:
        new_geometry = sly.Polygon(exterior=coords)
    ro_bbox_label = label.clone(
        geometry=new_geometry, obj_class=obj_class, tags=label.tags
    )
    return ro_bbox_label
