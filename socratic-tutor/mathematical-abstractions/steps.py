"""
Classes related to steps, axioms, and solutions
"""

import doctest
import abs_util
from abstractions import Axiom, Abstraction, AxSeqTreeRelPos


class Step:
    """
    Single action; can consist of one or more axioms
    Subclasses: AxStep and AbsStep
    """
    @staticmethod
    def from_string(step_str, AbsType=AxSeqTreeRelPos, ex_states=None):
        if '~' in step_str:
            return AbsStep.from_string(step_str, AbsType=AbsType, ex_states=ex_states)
        return AxStep.from_string(step_str, AbsType=AbsType, ex_states=ex_states)

    @staticmethod
    def from_name_idx_param(name, idx, param, AbsType=AxSeqTreeRelPos, ex_states=None, force_abs_step=False):
        if not isinstance(name, tuple):
            if force_abs_step:
                raise
            assert not isinstance(idx, tuple) and not isinstance(param, tuple)
            return AxStep(name, idx, param, AbsType, ex_states)
        assert isinstance(idx, tuple) and isinstance(param, tuple) and len(name) == len(idx) == len(param) > 1
        return AbsStep(tuple(Step.from_name_idx_param(name[i], idx[i], param[i]) for i in range(len(name))),
                       AbsType=AbsType, ex_states=ex_states, name=name, idx=idx, param=param)

    def __repr__(self):
        return f"{self.__class__.__name__}(\"{str(self)}\")"


class AxStep(Step):
    """
    Single-axiom action

    >>> Step.from_string("comm 3, (x + 2)").param
    '(x + 2)'
    >>> print(Step.from_string("refl").idx)
    None
    >>> str(Step.from_string("sub 1"))
    'sub 1'
    >>> str(AxStep("comm", 3, "(x + 2)"))
    'comm 3, (x + 2)'
    """

    def __init__(self, name, idx=None, param=None, AbsType=None, ex_states=None):
        self.ex_states = ex_states if ex_states is None else tuple(ex_states)

        self.name = name
        self.idx = idx
        self.param = param

        self.head_idx = self.tail_idx = self.idx

        self.name_str = self.name
        self.idx_str = '$' if self.idx is None else str(self.idx)
        self.param_str = '$' if self.param is None else self.param
        self.step_str = None

        self.axiom = Axiom(self.name, AbsType)

    @property
    def rule(self):
        return self.axiom

    @staticmethod
    def from_string(step_str, AbsType=None, ex_states=None):
        i = step_str.find(' ')
        if i == -1:
            ax_step = AxStep(step_str, AbsType=AbsType, ex_states=ex_states)
        else:
            name = step_str[:i]
            j = step_str.find(',')
            if j == -1:
                ax_step = AxStep(name, param=step_str[i+1:], AbsType=AbsType, ex_states=ex_states)
            else:
                ax_step = AxStep(name, idx=step_str[i+1:j], param=step_str[j+2:], AbsType=AbsType, ex_states=ex_states)
        ax_step.step_str = step_str
        return ax_step

    def __len__(self):
        return 1

    def __str__(self):
        if self.step_str is not None:
            return self.step_str
        if self.param is None:
            self.step_str = self.name
        elif self.idx is None:
            self.step_str = f"{self.name} {self.param}"
        else:
            self.step_str = f"{self.name} {self.idx}, {self.param}"
        return self.step_str


class AbsStep(Step):
    """
    Tuple of Step objects

    >>> step = AbsStep([AxStep("sub", param="y"), Step.from_string("refl~comm $~1, $~2x")])
    >>> step
    AbsStep("sub~{refl~comm} $~{$~1}, y~{$~2x}")
    >>> step.idx[1]
    (None, '1')
    >>> step.tail_idx
    '1'
    >>> step.flat_steps
    (AxStep("sub y"), AxStep("refl"), AxStep("comm 1, 2x"))
    >>> step2 = Step.from_string("sub~{refl~comm} $~{$~1}, y~{$~2x}")
    >>> step.idx
    (None, (None, '1'))
    >>> step2
    AbsStep("sub~{refl~comm} $~{$~1}, y~{$~2x}")
    >>> step2.steps
    (AxStep("sub y"), AbsStep("refl~comm $~1, $~2x"))
    >>> len(step2)
    3
    """

    def __init__(self, steps, AbsType=AxSeqTreeRelPos, ex_states=None, name=None, idx=None, param=None):
        assert isinstance(steps, (list, tuple))
        assert len(steps) > 1
        assert all(isinstance(step, Step) for step in steps)

        self.steps = tuple(steps)
        self.ex_states = ex_states if ex_states is None else tuple(ex_states)

        self.name = tuple(step.name for step in self.steps) if name is None else name
        self.idx = tuple(step.idx for step in self.steps) if idx is None else idx
        self.param = tuple(step.param for step in self.steps) if param is None else param
        self.strings_dict = {"name_str": None, "idx_str": None, "param_str": None}

        self.length = sum(len(step) for step in self.steps)
        self.flat_steps = sum(((step,) if isinstance(step, AxStep) else step.flat_steps for step in self.steps), ())

        self.head_idx = self.flat_steps[0].idx
        self.tail_idx = self.flat_steps[-1].idx

        self.abstraction = AbsType.from_steps(steps, self, ex_states)

    @property
    def rule(self):
        return self.abstraction

    @staticmethod
    def from_string(step_str, AbsType=AxSeqTreeRelPos, ex_states=None):
        i = step_str.index(' ')
        j = step_str.index(',')
        name_str = step_str[:i]
        idx_str = step_str[i+1:j]
        param_str = step_str[j+2:]

        def transform(x):
            if isinstance(x, str):
                return None if x == '$' else x
            return tuple(x)
        name = abs_util.split_to_tree(name_str, transform=transform)
        idx = abs_util.split_to_tree(idx_str, transform=transform)
        param = abs_util.split_to_tree(param_str, transform=transform)

        abs_step = Step.from_name_idx_param(name, idx, param, AbsType=AbsType, ex_states=ex_states, force_abs_step=True)
        abs_step.strings_dict = {"name_str": name_str, "idx_str": idx_str, "param_str": param_str}

        return abs_step

    @staticmethod
    def from_abs(ax_steps, abstraction, ex_states=None):
        """
        Given `ax_steps` and `abstraction`, return `AbsStep` object with `ax_steps`
        but tree structure given by `abstraction`
        """
        assert all(isinstance(step, AxStep) for step in ax_steps)
        assert isinstance(abstraction, Abstraction)
        assert len(ax_steps) == len(abstraction)
        # get indices for delimiting AxStep objects
        sub_abs_pos = [0]
        for sub_abs in abstraction.rules:
            sub_abs_pos.append(sub_abs_pos[-1] + len(sub_abs))
        # create AbsStep or AxStep objects
        steps = tuple(AbsStep.from_abs(ax_steps[sub_abs_pos[i]:sub_abs_pos[i+1]], abstraction=abstraction.rules[i])
                      if isinstance(abstraction.rules[i], Abstraction)
                      else ax_steps[sub_abs_pos[i]]
                      for i in range(len(abstraction.rules)))
        return AbsStep(steps, AbsType=abstraction.__class__, ex_states=ex_states)

    def __len__(self):
        return self.length

    @staticmethod
    def wrap_brkt(string, step):
        if isinstance(step, AbsStep):
            return '{' + string + '}'
        return string

    @property
    def name_str(self):
        if self.strings_dict["name_str"] is None:
            self.strings_dict["name_str"] = '~'.join(AbsStep.wrap_brkt(step.name_str, step) for step in self.steps)
        return self.strings_dict["name_str"]

    @property
    def idx_str(self):
        if self.strings_dict["idx_str"] is None:
            self.strings_dict["idx_str"] = '~'.join(AbsStep.wrap_brkt(step.idx_str, step) for step in self.steps)
        return self.strings_dict["idx_str"]

    @property
    def param_str(self):
        if self.strings_dict["param_str"] is None:
            self.strings_dict["param_str"] = '~'.join(AbsStep.wrap_brkt(step.param_str, step) for step in self.steps)
        return self.strings_dict["param_str"]

    def __str__(self):
        return f"{self.name_str} {self.idx_str}, {self.param_str}"

    def __iter__(self):
        """
        Iterates through all AxStep objects
        """
        for step in self.steps:
            if isinstance(step, AxStep):
                yield step
            else:
                yield from step

    def __lt__(self, other):
        return False


class Solution:
    """
    Solution stored as tuple of states (strings) and tuple of Step objects

    >>> sol = Solution.from_dict({"problem": "2x = 3", "solution": [{"state": "2x = 3", "action": "assumption"},
    ... {"state": "((x * 2) / 2) = (3 / 2)", "action": "div~comm $~2, 2~2x"}]})
    >>> sol.states
    ['2x = 3', '((x * 2) / 2) = (3 / 2)']
    >>> sol.actions[0].steps[1].param
    '2x'
    >>> sol.actions[0].steps
    (AxStep("div 2"), AxStep("comm 2, 2x"))
    >>> sol2 = Solution(["2x = 3", "((2x) / 2) = (3 / 2)", "((x * 2) / 2) = (3 / 2)", "(x * (2 / 2)) = (3 / 2)"],
    ... [Step.from_string("div 2"), Step.from_string("comm 0.0.0, 2x"), Step.from_string("assoc 0.0, (x * 2) / 2")])
    >>> print(sol2.display_compressed(abs_ax=AxSeqTreeRelPos.from_string("div~{comm~assoc:0_}:$_0.0.0")))
    div~{comm~assoc} $~{0.0.0~0.0}, 2~{2x~(x * 2) / 2}
    """

    def __init__(self, states, actions):
        assert all(isinstance(step, Step) for step in actions)
        assert len(states) == len(actions) + 1
        self.states = states
        self.actions = actions

    @staticmethod
    def from_dict(solution, AbsType=AxSeqTreeRelPos):
        """
        solution: {"problem": <str>, "solution": [{"state": <str>, "action": <str>}, ...]}
        """
        solution = solution["solution"]
        # list of string of states
        states = [step["state"] for step in solution]
        # list of Step objects (tuple of AxStep/Step objects)
        actions = [Step.from_string(solution[i]["action"], AbsType=AbsType, ex_states=states[i-1:i+1])
                   for i in range(1, len(solution))]
        return Solution(states, actions)


    def display_compressed(self, abs_ax=None):
        """
        Outputs compressed string with axioms and params (no states)
        Equivalent to string of corresponding AbsStep/AxStep object
        If `abs_ax` is given, the entire Solution object is taken to be
        an instance of that Rule and self.actions must be AxStep objects
        """
        if len(self.actions) == 1:
            step = self.actions[0]
            assert abs_ax is None or (isinstance(step, AxStep) and isinstance(abs_ax, Axiom)) 
            return str(step)
        return str(AbsStep.from_abs(self.actions, abs_ax))

    def __str__(self):
        return '\n'.join(self.states[i] + '\n\t' + str(self.actions[i]) for i in range(len(self.actions))) + '\n' + self.states[-1]

    def __repr__(self):
        return "Solution(" + ', '.join(repr(self.states[i]) + ', ' + repr(self.actions[i]) for i in range(len(self.actions))) + ', ' + repr(self.states[-1]) + ")"


if __name__ == "__main__":
    doctest.testmod()
