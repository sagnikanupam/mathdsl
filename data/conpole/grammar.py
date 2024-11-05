"""
conpole: grammar.py | Author : Sagnik Anupam

Utility functions for loading Python DSLs for the ConPoLe-based math domain. This grammar is taken from the action space of the ConPoLe paper and can be found in the dreamcoder/conpole domain.
"""
from collections import OrderedDict

from src.models.model_loaders import ModelLoaderRegistries, GRAMMAR, ModelLoader
from src.models.laps_grammar import LAPSGrammar

import dreamcoder.domains.conpole.conpoleMathPrimitives as conpolePrimitives

GrammarRegistry = ModelLoaderRegistries[GRAMMAR]
LARGEST_CONSTANT = 10 #Largest constant encoded in the math domain, must be between 0 and 25

@GrammarRegistry.register
class ConpoleGrammarLoader(ModelLoader):
    """Loads the math grammar for ConPoLe experiments.
    """

    name = "conpole"  # Special handler for OCaml enumeration.

    def load_model(self, experiment_state):
        math_primitives = list(
            OrderedDict((x, True) for x in conpolePrimitives.mathPrimitives(LARGEST_CONSTANT)).keys()
        )
        grammar = LAPSGrammar.uniform(math_primitives)
        return grammar