"""
Classes for types of abstractions
"""

import doctest
import abs_util


class Rule:
    @staticmethod
    def from_string(rule_str, abs_type=None):
        if '~' not in rule_str:
            return Axiom(rule_str, ABS_TYPES[abs_type])
        else:
            return ABS_TYPES[abs_type].from_string(rule_str)


class Axiom(Rule):
    def __init__(self, name, AbsType=None):
        self.name = name
        self.AbsType = AbsType
        self.height = 0

    def __iter__(self):
        yield self.AbsType.get_abs_elt_from_ax(self)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Axiom(\"{self.name}\")"

    def __eq__(self, other):
        return isinstance(other, Axiom) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __len__(self):
        return 1


class Abstraction(Rule):
    def __init__(self, rules, ex_step=None, ex_states=None):
        assert isinstance(rules, (list, tuple))
        assert len(rules) > 1
        assert all(isinstance(rule, Rule) for rule in rules)
        self.rules = tuple(rules)
        self.ex_step = ex_step
        self.ex_states = None if ex_states is None else tuple(ex_states)
        self.ex_steps = None  # only for initializing with `from_steps` method

        self.length = sum(len(rule) for rule in self.rules)
        self.height = 1 + max(rule.height for rule in self.rules)

        self.name_str = None
        self.freq = None
        self.score = None

    @staticmethod
    def from_string(abs_str, ex_step=None, ex_states=None):
        raise NotImplementedError()

    @staticmethod
    def from_steps(steps, ex_step=None, ex_states=None):
        raise NotImplementedError()

    @staticmethod
    def from_abs_elt(abs_elts, ex_step=None, ex_states=None):
        raise NotImplementedError()

    @staticmethod
    def from_shifted_abs_elt(abs_elts, ex_step=None, ex_states=None):
        raise NotImplementedError()

    @staticmethod
    def get_abs_elt(next_step, cur_steps):
        """
        Gets abstraction element corresponding to `next_step`, given `cur_steps`
        """
        raise NotImplementedError()

    @staticmethod
    def get_abs_elt_from_ax(ax: Axiom):
        """
        Gets abstraction element corresponding to a single axiom `ax`
        """
        raise NotImplementedError()

    @staticmethod
    def get_ax_from_abs_elt(abs_elt):
        """
        Gets axiom corresponding to an abstraction element `abs_elt`
        """
        raise NotImplementedError()

    def __iter__(self):
        """
        Allows iteration through the constituents of the abstraction
        """
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return f'{self.__class__.__name__}("{str(self)}")'

    def __eq__(self, other):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()

    def __len__(self):
        return self.length


class AxiomSeq(Abstraction):
    """
    Abstraction: sequence of rules

    >>> from steps import *; from abstractions import *
    >>> AxiomSeq.from_steps([Step.from_string("refl"), AbsStep((Step.from_string("sub 1"), Step.from_string("comm 0.0.1, 3x")), AxiomSeq), Step.from_string("comm 0.1, 2x")]).rules
    (Axiom("refl"), AxiomSeq("sub~comm"), Axiom("comm"))
    >>> AxiomSeq.from_string("assoc~eval").rules
    (Axiom("assoc"), Axiom("eval"))
    >>> print(AxiomSeq.from_string("{{sub~{assoc~eval}}~eval}~{comm~{{div~{assoc~eval}}~{mul1~eval}}}").rules[0].rules)
    (AxiomSeq("sub~{assoc~eval}"), Axiom("eval"))
    """

    @staticmethod
    def from_string(abs_str, ex_step=None, ex_states=None):
        def transform(component):
            if isinstance(component, str):
                return Axiom(component, AxiomSeq)
            return AxiomSeq(component)
        abstraction = abs_util.split_to_tree(abs_str, transform=transform)
        abstraction.ex_step = ex_step
        abstraction.ex_states = ex_states
        return abstraction

    @staticmethod
    def from_steps(steps, ex_step=None, ex_states=None):
        rules = tuple(step.rule for step in steps)
        abstraction = AxiomSeq(rules, ex_step, ex_states)
        abstraction.ex_steps = steps
        return abstraction

    @staticmethod
    def from_abs_elt(abs_elts, ex_step=None, ex_states=None):
        return AxiomSeq(tuple(abs_elts), ex_step, ex_states)

    @staticmethod
    def from_shifted_abs_elt(abs_elts, ex_step=None, ex_states=None):
        return AxiomSeq(tuple(abs_elts), ex_step, ex_states)

    @staticmethod
    def get_abs_elt(next_step, cur_steps):
        return next_step.rule

    @staticmethod
    def get_abs_elt_from_ax(ax: Axiom):
        return ax

    @staticmethod
    def get_ax_from_abs_elt(abs_elt):
        return abs_elt

    def __iter__(self):
        for rule in self.rules:
            if isinstance(rule, Axiom):
                yield rule
            else:
                assert isinstance(rule, AxiomSeq)
                yield from rule.rules

    def __str__(self):
        if self.name_str is None:
            def get_name_str(rule):
                if isinstance(rule, Axiom):
                    return rule.name
                return '{' + str(rule) + '}'
            self.name_str = '~'.join(map(get_name_str, self.rules))
        return self.name_str

    def __eq__(self, other):
        return isinstance(other, AxiomSeq) and self.rules == other.rules

    def __hash__(self):
        return hash(self.rules)


class AxSeqTreeRelPos(Abstraction):
    """
    Abstraction: sequence of rules + relative positions of application within tree
    Corresponding Step objects have bit strings as their indices

    >>> from steps import *; from abstractions import *
    >>> AxSeqTreeRelPos.from_steps([Step.from_string("refl"), AbsStep((Step.from_string("sub 1"), Step.from_string("comm 0.0.1, 3x"))), Step.from_string("comm 0.1, 2x")]).rel_pos
    ((None, None), ('0.1', '1'))
    >>> AxSeqTreeRelPos.from_string("assoc~eval:_1").rel_pos
    (('', '1'),)
    >>> print(AxSeqTreeRelPos.from_string("{{sub~{assoc~eval:_1}:$_0.0}~eval:0_1}~{comm~{{div~{assoc~eval:_1}:$_0.0}~{mul1~eval:0_1}:_}:_}:_").rules[0].rules)
    (AxSeqTreeRelPos("sub~{assoc~eval:_1}:$_0.0"), Axiom("eval"))
    """

    def __init__(self, rules, rel_pos, ex_step=None, ex_states=None):
        super().__init__(rules, ex_step, ex_states)
        self.rel_pos = rel_pos
        self.pos_str = None
        
    @staticmethod
    def from_string(abs_str, ex_step=None, ex_states=None):
        def transform(component, info=None):
            if isinstance(component, str):
                return Axiom(component, AxSeqTreeRelPos)
            split_pos_str = info.split('~')
            rel_pos = tuple(tuple(map(lambda x: None if x == '$' else x, pos.split('_'))) for pos in split_pos_str)
            return AxSeqTreeRelPos(component, rel_pos)
        abstraction = abs_util.split_to_tree(abs_str, transform=transform, info_mark=':')
        abstraction.ex_step = ex_step
        abstraction.ex_states = ex_states
        return abstraction

    @staticmethod
    def from_steps(steps, ex_step=None, ex_states=None):
        rules = tuple(step.rule for step in steps)
        rel_pos = tuple(AxSeqTreeRelPos.remove_prefix(steps[i].tail_idx, steps[i+1].head_idx)
                        for i in range(len(steps)-1))
        abstraction = AxSeqTreeRelPos(rules, rel_pos, ex_step, ex_states)
        abstraction.ex_steps = steps
        return abstraction

    @staticmethod
    def from_abs_elt(abs_elts, ex_step=None, ex_states=None):
        """
        See `get_abs_elt` and `__iter__` for specification for `abs_elts`

        >>> from abstractions import *
        >>> AxSeqTreeRelPos.from_abs_elt([(None, Axiom("hi")), (('', ''), Axiom("my")), (('1', '0'), Axiom("name")), (('0.1', '1'), Axiom("is")), (('1.0', '0.0'), Axiom("Zhening"))])
        AxSeqTreeRelPos("hi~my~name~is~Zhening:_~1_0~0.1_1~1.0_0.0")
        """
        rel_pos, rules = zip(*abs_elts)
        return AxSeqTreeRelPos(rules, rel_pos[1:], ex_step, ex_states)

    @staticmethod
    def from_shifted_abs_elt(abs_elts, ex_step=None, ex_states=None):
        """
        `abs_elts` are 'shifted' (see test case)

        >>> from abstractions import *
        >>> AxSeqTreeRelPos.from_shifted_abs_elt([(Axiom("hi"), ('', '')), (Axiom("my"), ('1', '0')), (Axiom("name"), ('0.1', '1')), (Axiom("is"), ('1.0', '0.0')), (Axiom("Zhening"), None)])
        AxSeqTreeRelPos("hi~my~name~is~Zhening:_~1_0~0.1_1~1.0_0.0")
        """
        rules, rel_pos = zip(*abs_elts)
        return AxSeqTreeRelPos(rules, rel_pos[:-1], ex_step, ex_states)

    @staticmethod
    def remove_prefix(idx1, idx2):
        """
        Given idx1 and idx2 (strings of bits), remove maximal common prefix
        """
        if idx1 is None:
            if idx2 is None:
                return None, None
            return None, idx2
        if idx2 is None:
            return idx1, None
        i = 0
        while i < len(idx1) and i < len(idx2) and idx1[i] == idx2[i]:
            i += 2  # specifically for bit string including periods separating indicees
        return idx1[i:], idx2[i:]

    @staticmethod
    def get_abs_elt(next_step, cur_steps):
        """
        `cur_steps` is Solution object

        >>> from steps import Step, Solution
        >>> AxSeqTreeRelPos.get_abs_elt(Step.from_string("eval 0.0.0.1, 3 - 3"), Solution(["", ""], [Step.from_string("assoc 0.0.0, (x + 3) - 3")]))
        (('', '1'), Axiom("eval"))
        """
        if len(cur_steps.actions) == 0:
            return (None, next_step.rule)
        last_step = cur_steps.actions[-1]
        return (AxSeqTreeRelPos.remove_prefix(last_step.tail_idx, next_step.head_idx), next_step.rule)

    @staticmethod
    def get_abs_elt_from_ax(ax: Axiom):
        return (None, ax)

    @staticmethod
    def get_ax_from_abs_elt(abs_elt):
        return abs_elt[1]

    def __iter__(self, prev_rel_pos=None):
        """
        >>> seq = AxSeqTreeRelPos.from_string("comm~assoc~{eval~comm:1_}~{sub~eval:$_0.1}:0_~_1~0_$")
        >>> for elt in seq:
        ...     print(elt)
        ...
        (None, Axiom("comm"))
        (('0', ''), Axiom("assoc"))
        (('', '1'), Axiom("eval"))
        (('1', ''), Axiom("comm"))
        (('0', None), Axiom("sub"))
        ((None, '0.1'), Axiom("eval"))
        """
        if isinstance(self.rules[0], Axiom):
            yield (prev_rel_pos, self.rules[0])
        else:
            assert isinstance(self.rules[0], AxSeqTreeRelPos)
            yield from self.rules[0].__iter__(prev_rel_pos)
        for i in range(1, len(self.rules)):
            if isinstance(self.rules[i], Axiom):
                yield (self.rel_pos[i-1], self.rules[i])
            else:
                assert isinstance(self.rules[i], AxSeqTreeRelPos)
                yield from self.rules[i].__iter__(self.rel_pos[i-1])

    def __str__(self):
        if self.name_str is None:
            def get_name_str(rule):
                if isinstance(rule, Axiom):
                    return rule.name
                return '{' + str(rule) + '}'
            self.name_str = '~'.join(map(get_name_str, self.rules))
        if self.pos_str is None:
            def get_pos_str(pos):
                str1 = '$' if pos[0] is None else pos[0]
                str2 = '$' if pos[1] is None else pos[1]
                return str1 + '_' + str2
            self.pos_str = '~'.join(map(get_pos_str, self.rel_pos))
        return f"{self.name_str}:{self.pos_str}"

    def __eq__(self, other):
        return isinstance(other, AxSeqTreeRelPos) and self.rules == other.rules and self.rel_pos == other.rel_pos

    def __hash__(self):
        return hash(self.rules) ^ hash(self.rel_pos)


ABS_TYPES = {"ax_seq": AxiomSeq, "tree_rel_pos": AxSeqTreeRelPos}


if __name__ == "__main__":
    doctest.testmod()
