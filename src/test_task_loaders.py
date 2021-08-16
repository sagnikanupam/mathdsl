"""
test_task_loaders.py | Author : Catherine Wong
Utility classes for loading and batching datasets of tasks and language.
"""
from src.task_loaders import *

from src.experiment_iterator import *
from src.test_experiment_iterator import TEST_GRAPHICS_CONFIG


def test_ordered_task_batcher():
    test_config = TEST_GRAPHICS_CONFIG
    test_experiment_state = ExperimentState(test_config)

    task_batcher = OrderedTaskBatcher(
        test_experiment_state, curr_iteration=None, max_iterations=None
    )