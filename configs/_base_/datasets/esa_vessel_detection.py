# dataset settings
dataset_type = 'CocoDataset'
data_root = '/home/roberto/PythonProjects/S2RAWVessel/mmdetection/data/S2ESA/'

# Modify dataset related settings
metainfo = {
    'classes': ('Vessel', ),
    'palette': [
        (220, 20, 60),
    ]
}

backend_args = None
IMG_SCALE = (2816, 2816)

train_pipeline = [
    dict(type='LoadImageFromFile',to_float32=True, color_type='color', imdecode_backend='pillow', backend_args=backend_args),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', scale=IMG_SCALE, keep_ratio=True),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(type='RandomFlip', prob=0.5, direction='vertical'),
    dict(type='PackDetInputs')
]
test_pipeline = [
    dict(type='LoadImageFromFile',to_float32=True, color_type='color', imdecode_backend='pillow', backend_args=backend_args),
    dict(type='Resize', scale=IMG_SCALE, keep_ratio=True),
    # If you don't have a gt annotation, delete the pipeline
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor'))
]
train_dataloader = dict(
    batch_size=2,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        ann_file='annotations/train.json',
        data_prefix=dict(img='imgs/'),
        filter_cfg=dict(filter_empty_gt=True), # , min_size=32
        pipeline=train_pipeline,
        backend_args=backend_args))
val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        ann_file='annotations/val.json',
        data_prefix=dict(img='imgs/'),
        test_mode=True,
        pipeline=test_pipeline,
        backend_args=backend_args))
# format the output results for submission.
test_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        metainfo=metainfo,
        ann_file=data_root + 'annotations/test.json',
        data_prefix=dict(img='imgs/'),
        test_mode=True,
        pipeline=test_pipeline))

val_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'annotations/val.json',
    metric='bbox',
    format_only=False,
    backend_args=backend_args)
test_evaluator = dict(
    type='CocoMetric',
    metric='bbox',
    format_only=True,
    ann_file=data_root + 'annotations/test.json',
    outfile_prefix='./work_dirs/esa_v2_detection/test_results/')