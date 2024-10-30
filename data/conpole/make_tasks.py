"""
conpole : make_tasks.py | Author : Sagnik Anupam.

Utility functions for loading tasks for the ConPoLe math domain. This grammar is taken from the action space of the ConPoLe paper and can be found in the dreamcoder/conpole domain.
"""

import os

from src.task_loaders import *
from data.math.grammar import *

import dreamcoder.domains.math.makeMathTasks as math_legacy

DOMAIN_NAME = "math"
ROOT_DIR = os.getcwd()
DEFAULT_DATA_DIRECTORY = os.path.join(ROOT_DIR, f"dreamcoder/data/{DOMAIN_NAME}")
TASKS = "cognitiveTutor"
DEFAULT_TASKS_DIRECTORY = os.path.join(DEFAULT_DATA_DIRECTORY, TASKS)


@TaskLoaderRegistry.register
class ConpoleLoader(TaskDataLoader):
    name = "conpole"

    def load_tasks(self):

        train_tasks, test_tasks = math_legacy.loadMathDataset(
            task_dataset=TASKS,
            task_dataset_dir=DEFAULT_DATA_DIRECTORY,
            type_request="tstr",
        )

        return {TRAIN: train_tasks, TEST: test_tasks}
    

@TaskLanguageLoaderRegistry.register
class ConpoleLanguageLoader(TaskDataLoader):
    name = "conpole"

    def load_task_language(self):
        return ({},{}) # No language for math tasks
    

