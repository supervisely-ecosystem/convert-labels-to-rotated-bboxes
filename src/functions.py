import cv2
import numpy as np
import supervisely as sly

from src.globals import KEEP_ANNS, PROJECT_ID, PROJECT_NAME, WORKSPACE_ID


def create_project(api: sly.Api):
    src_project_meta = sly.ProjectMeta.from_json(
        data=api.project.get_meta(id=PROJECT_ID)
    )
    ro_bbox_obj_classes = [
        sly.ObjClass(
            name=f"ro_bbox_{obj_class.name}",
            geometry_type=sly.Polygon,
            color=obj_class.color,
        )
        for obj_class in src_project_meta.obj_classes
    ]

    dst_project_meta = sly.ProjectMeta(obj_classes=ro_bbox_obj_classes)
    if KEEP_ANNS is True:
        dst_project_meta = dst_project_meta.merge(other=src_project_meta)

    dst_project = api.project.create(
        workspace_id=WORKSPACE_ID,
        name=PROJECT_NAME or None,
        type=sly.ProjectType.IMAGES,
        change_name_if_conflict=True,
    )
    api.project.update_meta(id=dst_project.id, meta=dst_project_meta.to_json())
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
    ann_infos = api.annotation.get_list(dataset_id=ds_id)
    ann_jsons = [ann_info.annotation for ann_info in ann_infos]
    anns = [
        sly.Annotation.from_json(data=ann_json, project_meta=project_meta)
        for ann_json in ann_jsons
    ]
    return anns


def label_to_ro_bbox(label: sly.Label, project_meta: sly.ProjectMeta):
    if label.geometry == sly.Rectangle:
        return label

    ro_bbox_obj_class_name = f"ro_bbox_{label.obj_class.name}"
    ro_bbox_obj_class = project_meta.get_obj_class(ro_bbox_obj_class_name)

    if label.geometry != sly.Polygon:
        new_geometry = label.geometry.convert(new_geometry=sly.Polygon)[0]
        label = sly.Label(geometry=new_geometry, obj_class=ro_bbox_obj_class)

    poly_ext = label.geometry.exterior

    points = []
    for coord in poly_ext:
        coords = np.array([coord.col, coord.row])
        points.append(coords)

    points = np.array(points)

    rect = cv2.minAreaRect(points)
    box = cv2.boxPoints(rect)
    rot_box = np.int0(box)

    coords = [[coord[1], coord[0]] for coord in rot_box]
    ro_bbox_poly = sly.Polygon(exterior=coords)
    ro_bbox_label = sly.Label(geometry=ro_bbox_poly, obj_class=ro_bbox_obj_class)
    return ro_bbox_label
