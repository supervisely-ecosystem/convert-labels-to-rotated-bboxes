import supervisely as sly

from src.functions import (
    copy_ds_images,
    create_project,
    get_anns_list,
    label_to_ro_bbox,
)
from src.globals import DATASET_ID, KEEP_ANNS, PROJECT_ID, api, app

dst_project, dst_project_meta, src_project_meta = create_project(api=api)
if DATASET_ID is not None:
    datasets = [api.dataset.get_info_by_id(id=DATASET_ID)]
else:
    datasets = api.dataset.get_list(project_id=PROJECT_ID)

progress = sly.Progress(message="Uploading annotations", total_cnt=len(datasets))
for dataset in datasets:
    dst_dataset = api.dataset.create(
        project_id=dst_project.id, name=dataset.name, change_name_if_conflict=True
    )

    images_ids = copy_ds_images(api, src_ds_id=dataset.id, dst_ds_id=dst_dataset.id)
    anns = get_anns_list(api=api, ds_id=dataset.id, project_meta=src_project_meta)

    ro_bbox_anns = []
    for ann in anns:
        ro_bbox_labels = []
        for label in ann.labels:
            ro_bbox_label = label_to_ro_bbox(label=label, project_meta=dst_project_meta)
            ro_bbox_labels.append(ro_bbox_label)
        if KEEP_ANNS:
            ro_bbox_anns.append(ann.add_labels(labels=ro_bbox_labels))
        else:
            ro_bbox_anns.append(ann.clone(labels=ro_bbox_labels))

    for batch_images_ids, batch_ro_bbox_anns in zip(
        sly.batched(images_ids), sly.batched(ro_bbox_anns)
    ):
        api.annotation.upload_anns(img_ids=batch_images_ids, anns=batch_ro_bbox_anns)
    progress.iter_done_report()

app.shutdown()
