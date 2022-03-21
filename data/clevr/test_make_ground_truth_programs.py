"""
test_make_ground_truth_programs.py
"""
from src.task_loaders import *
import dreamcoder.domains.clevr.makeClevrTasks as makeClevrTasks

from data.clevr.make_tasks import *
import data.clevr.make_ground_truth_programs as to_test

possible_dict_keys = [
    "1_zero_hop",
    "2_transform",
    "1_same_relate_restricted",
    "2_remove",
    "1_single_or",
    "1_one_hop",
    "2_localization",
    "1_compare_integer",
]


def get_clevr_tasks(task_datasets=["all"]):
    args = {
        "curriculumDatasets": [],
        "taskDatasets": task_datasets,
        "taskDatasetDir": DEFAULT_TASK_DATASET_DIR,
        "languageDatasetDir": DEFAULT_LANGUAGE_DIR,
    }
    (
        train_tasks,
        test_tasks,
        language_dataset,
    ) = makeClevrTasks.loadAllTaskAndLanguageDatasets(args)
    tasks = {TRAIN: train_tasks, TEST: test_tasks}
    return tasks


def test_ground_truth_localization():
    tasks = get_clevr_tasks(task_datasets=["2_localization",])
    for k in tasks.keys():
        for task in tasks[k]:
            make_ground_truth_program_for_task(task)

