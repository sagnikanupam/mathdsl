from dreamcoder.program import Primitive
from dreamcoder.type import arrow, tint, tstr
import math
from dreamcoder.domains.conpole.conpoleMathPrimitives import (
    _refl, _comm, _assoc, _dist, _subcomm, _eval, _addzero, _subzero, _multone, _divone, _divself, _subself, _subsub, _multzero, _zerodiv, _add, _sub, _mult, _div, _newConstGen, _op, _treeOp, _genSub, detreefy, treefy
)

ops = ["+", "-", "*", "/"]

def _assoc_eval_add0Helper(s):
    s1 = _assoc(s, 0)
    eqTree = treefy(s1)
    if eqTree.left != "None" and eqTree.right!="None":
        return _addzero(_eval(s1, len(_genSub(detreefy(eqTree.left)))+1), 0)
    return s

def _assoc_eval_eval_add0Helper(s):
    eqTree = treefy(s)
    if eqTree!= "None" and eqTree.left != "None" and eqTree.right != "None" and eqTree.left.left != "None":
        s1 = _assoc(s, 1)
        s2 = _eval(s1, len(_genSub(detreefy(treefy(s1).left.left)))+2)
        s3 = _eval(s2, len(_genSub(detreefy(treefy(s2).left)))+1)
        return _addzero(s3, 1)
    return s

def _dist_dist_eval_eval_eval_eval_multoneHelper(s):
    eqTree = treefy(s)
    if eqTree!= "None" and eqTree.left != "None" and eqTree.left.left!= "None" and eqTree.left.left.left!= "None" and eqTree.right != "None" and eqTree.right.left != "None":
        s1 = _dist(s, 2)
        s2 = _dist(s1, 1)
        s3 = _eval(s2, len(_genSub(detreefy(treefy(s2).left))) + 2)
        s4 = _eval(s3, len(_genSub(detreefy(treefy(s3).left))) + 1)
        s5 = _eval(s4, 3)
        s6 = _eval(s5, 2)
        return _multone(s6, 1)
    return s

def _eval_evalHelper(s):
    eqTree = treefy(s)
    if eqTree!= "None" and eqTree.left != "None":
        s1 = _eval(s, 1)
        return _eval(s1, 0)
    return s

def _assoc_eval_add0(s, i):
    return _treeOp(s, i, _assoc_eval_add0Helper)

def _assoc_eval_eval_add0(s, i):
    return _treeOp(s, i, _assoc_eval_eval_add0Helper)

def _dist_dist_eval_eval_eval_eval_multone(s, i):
    return _treeOp(s, i, _dist_dist_eval_eval_eval_eval_multoneHelper)

def _eval_eval(s, i):
    return _treeOp(s, i, _eval_evalHelper)

def _sub_eval_comm(s, x):
    s1 = _sub(s, x)
    s2 = _eval(s1, len(_genSub(detreefy(treefy(s1).left)))+1)
    eqTree = treefy(s2)
    if eqTree != "None" and eqTree.left != "None" and eqTree.left.left != "None":
        return _comm(s2, 2)
    return s

def _add_eval_comm_assoc_comm(s, x):
    s1 = _add(s, x)
    eqTree1 = treefy(s1)
    if eqTree1 != "None" and eqTree1.left!= "None":
        s2 = _eval(s1, len(_genSub(detreefy(eqTree1.left)))+1)
        s3 = _comm(s2, 1)
        s4 = _assoc(s3, 1)
        eqTree2 = treefy(s4)
        if eqTree2 != "None" and eqTree2.left!= "None" and eqTree2.left.left!= "None":
            return _comm(s4, 2)
    return s

def _sub_eval_comm_assoc_eval_add0(s, x):
    s1 = _sub_eval_comm(s, x)
    eqTree = treefy(s1)
    if eqTree!="None" and eqTree.left != "None":
        return _assoc_eval_add0(s1, 1)
    return s
    
def _add_eval_comm_assoc_comm_assoc_eval_add0(s, x):
    s1 = _add_eval_comm_assoc_comm(s, x)
    eqTree = treefy(s1)
    if eqTree!="None" and eqTree.left != "None":
        return _assoc_eval_add0(s1, 1)
    return s 
    
def _sub_assoc_eval_eval_add0(s, x):
    s1 = _sub(s, x)
    eqTree = treefy(s1)
    if eqTree != "None" and eqTree.left != "None" and eqTree.left.left != "None":
        return _assoc_eval_eval_add0(s1, 0)
    return s

def _sub_assoc_eval_eval_add0_multone(s, x):
    s1 = _sub_assoc_eval_eval_add0(s, x)
    eqTree = treefy(s1)
    if eqTree != "None" and eqTree.left != "None":
        return _multone(s1, 1)
    return s
    
def _sub_subsub_comm_assoc_eval_eval_add0_multone(s, x):
    s1 = _sub(s, x)
    eqTree = treefy(s1)
    if eqTree != "None" and eqTree.left != "None" and eqTree.left.left != "None":
        s2 = _subsub(s1, 2)
        s3 = _comm(s2, 2)
        s4 = _assoc_eval_eval_add0(s3, 0)
        return _multone(s4, 1)
    return s

def _div_eval_comm_assoc_eval_multone(s, x):
    s1 = _div(s, x)
    eqTree = treefy(s1)
    if eqTree != "None" and eqTree.left != "None" and eqTree.left.left != "None":
        s2 = _eval(s1, len(_genSub(detreefy(eqTree.left)))+1)
        s3 = _comm(s2, 2)
        s4 = _assoc(s3, 1)
        s5 = _eval(s4, len(_genSub(detreefy(treefy(s4).left.left)))+2)
        return _multone(s5, 1)
    return s
    
def _div_comm_assoc_eval(s, x):
    s1 = _div(s, x)
    eqTree = treefy(s1)
    if eqTree != "None" and eqTree.left != "None" and eqTree.left.left != "None":
        s2 = _comm(s1, 2)
        s3 = _assoc(s2, 1)
        return _eval(s3, len(_genSub(detreefy(treefy(s3).left.left)))+2)
    return s
    
def _div_comm_assoc_eval_eval_multone(s, x):
    s1 = _div(s, x)
    eqTree = treefy(s1)
    if eqTree != "None" and eqTree.left != "None" and eqTree.left.left != "None":
        s2 = _comm(s1, 2)
        s3 = _assoc(s2, 1)
        s4 = _eval(s3, len(_genSub(detreefy(treefy(s3).left)))+1)
        s5 = _eval(s4, len(_genSub(detreefy(treefy(s4).left.left)))+2)
        return _multone(s5, 1)    
    return s

def _sub_dist_comm_assoc_subself_eval(s, x):
    s1 = _sub(s, x)
    eqTree = treefy(s1)
    if eqTree != "None" and eqTree.left != "None" and eqTree.left.left != "None" and eqTree.right != "None" and eqTree.right.left != "None" and eqTree.right.right != "None":
        s2 = _dist(s1, 1)
        s3 = _comm(s2, len(_genSub(detreefy(treefy(s2).left)))+2)
        s4 = _assoc(s3, len(_genSub(detreefy(treefy(s3).left)))+1)
        s5 = _subself(s4, len(_genSub(detreefy(treefy(s4).left)))+2+len(_genSub(detreefy(treefy(s4).right.left))))
        return _eval(s5, 2)
    return s

def mathPrimitives(LARGEST_CONSTANT: int = 10):
    '''
    The largest constant determines the largest constant which is encoded as a primitive in the domain.
    '''
    return [
        Primitive("conpole_refl", arrow(tstr, tint, tstr), _refl),
        Primitive("conpole_comm", arrow(tstr, tint, tstr), _comm),
        Primitive("conpole_assoc", arrow(tstr, tint, tstr), _assoc),
        Primitive("conpole_dist", arrow(tstr, tint, tstr), _dist),
        Primitive("conpole_subcomm", arrow(tstr, tint, tstr), _subcomm),
        Primitive("conpole_eval", arrow(tstr, tint, tstr), _eval),
        Primitive("conpole_addzero", arrow(tstr, tint, tstr), _addzero),
        Primitive("conpole_subzero", arrow(tstr, tint, tstr), _subzero),
        Primitive("conpole_multone", arrow(tstr, tint, tstr), _multone),
        Primitive("conpole_divone", arrow(tstr, tint, tstr), _divone),
        Primitive("conpole_divself", arrow(tstr, tint, tstr), _divself),
        Primitive("conpole_subself", arrow(tstr, tint, tstr), _subself),
        Primitive("conpole_subsub", arrow(tstr, tint, tstr), _subsub),
        Primitive("conpole_multzero", arrow(tstr, tint, tstr), _multzero),
        Primitive("conpole_zerodiv", arrow(tstr, tint, tstr), _zerodiv),
        Primitive("conpole_add", arrow(tstr, tint, tstr), _add),
        Primitive("conpole_sub", arrow(tstr, tint, tstr), _sub),
        Primitive("conpole_mult", arrow(tstr, tint, tstr), _mult),
        Primitive("conpole_div", arrow(tstr, tint, tstr), _div),
        Primitive("conpole_newConstGen", arrow(tint, tint, tint, tint), _newConstGen),
        Primitive("lemma_assoc_eval_add0", arrow(tstr, tint, tstr), _assoc_eval_add0),
        Primitive("lemma_assoc_eval_eval_add0", arrow(tstr, tint, tstr), _assoc_eval_eval_add0),
        Primitive("lemma_sub_eval_comm", arrow(tstr, tint, tstr), _sub_eval_comm),
        Primitive("lemma_dist_dist_eval_eval_eval_eval_multone", arrow(tstr, tint, tstr), _dist_dist_eval_eval_eval_eval_multone),
        Primitive("lemma_add_eval_comm_assoc_comm", arrow(tstr, tint, tstr), _add_eval_comm_assoc_comm),
        Primitive("lemma_sub_eval_comm_assoc_eval_add0", arrow(tstr, tint, tstr), _sub_eval_comm_assoc_eval_add0),
        Primitive("lemma_add_eval_comm_assoc_comm_assoc_eval_add0", arrow(tstr, tint, tstr), _add_eval_comm_assoc_comm_assoc_eval_add0),
        Primitive("lemma_sub_assoc_eval_eval_add0_multone", arrow(tstr, tint, tstr), _sub_assoc_eval_eval_add0_multone),
        Primitive("lemma_sub_assoc_eval_eval_add0", arrow(tstr, tint, tstr), _sub_assoc_eval_eval_add0),
        Primitive("lemma_sub_subsub_comm_assoc_eval_eval_add0_multone", arrow(tstr, tint, tstr), _sub_subsub_comm_assoc_eval_eval_add0_multone),
        Primitive("lemma_div_eval_comm_assoc_eval_multone", arrow(tstr, tint, tstr), _div_eval_comm_assoc_eval_multone),
        Primitive("lemma_div_comm_assoc_eval", arrow(tstr, tint, tstr), _div_comm_assoc_eval),
        Primitive("lemma_div_comm_assoc_eval_eval_multone", arrow(tstr, tint, tstr), _div_comm_assoc_eval_eval_multone),
        Primitive("lemma_sub_dist_comm_assoc_subself_eval", arrow(tstr, tint, tstr), _sub_dist_comm_assoc_subself_eval),
        Primitive("lemma_eval_eval", arrow(tstr, tint, tstr), _eval_eval),
    ] + [Primitive("mathDomain_"+str(x), tint, x) for x in range(0, LARGEST_CONSTANT+1)]

if __name__ == "__main__":
    print(_refl(detreefy(treefy("(= (-7) (- (3) (/ (-7) (x))))")), 0))
    print(_subcomm("(= (-7) (- (3) (- (-7) (x))))", 2))
    print(_assoc("(= (-7) (+ (3) (- (-7) (x))))", 2))
    print(_dist("(= (-7) (* (3) (- (-7) (x))))", 2))
    print(_dist("(= (-7) (- (* (3) (-7)) (* (3) (x))))", 2))
    print(_multzero(_mult(_subself(_sub("(= (-7) (- (3) (/ (-7) (x))))", 1), 1), 1), 4))
    print(_zerodiv(_div(_subself(_sub("(= (-7) (- (3) (/ (-7) (x))))", 1), 1), 1), 1))
    print(_subsub(_add("(= (-7) (- (3) (/ (-7) (x))))", 1), 1))
    print(_comm(_mult("(= (-7) (- (3) (/ (-7) (x))))", 1), 4))
    print(_divself(_div("(= (-7) (- (3) (/ (-7) (x))))", 1), 1))
    print(_addzero("(= (-7) (+ (0) (/ (-7) (x))))", 2))
    print(_subzero("(= (-7) (- (3) (0)))", 2))
    print(_eval("(= (-7) (- (3) (0)))", 2))
    print(_multone("(= (-7) (* (x) (1)))", 2))
    print(_divone("(= (-7) (/ (x) (1)))", 2))
    """
    Expected Test Results:
    (= (- (3) (/ (-7) (x))) (-7))
    (= (-7) (- (3) (- (-7) (x))))
    (= (-7) (- (+ (3) (-7)) (x)))
    (= (-7) (- (* (3) (-7)) (* (3) (x))))
    (= (-7) (* (- (-7) (x)) (3)))
    (= (* (0) (0)) (0))
    (= (0) (/ (- (- (3) (/ (-7) (x))) (-7)) (0)))
    (= (- (-7) (7)) (+ (- (3) (/ (-7) (x))) (-7)))
    (= (* (-7) (-7)) (* (-7) (- (3) (/ (-7) (x)))))
    (= (1) (/ (- (3) (/ (-7) (x))) (-7)))
    (= (-7) (/ (-7) (x)))
    (= (-7) (3))
    (= (-7) (3))
    (= (-7) (x))
    (= (-7) (x)) 
    """
    
    # Test that problems not solved by DC-Conpole in iterations 1 and 2 are solvable in the DSL

    print(_eval(_multone(_eval(_dist("(= (+ (* (-1) (x)) (* (2) (x))) (+ (-3) (4)))", 1), 2), 1), 2))
    print(_eval(_addzero(_eval(_assoc(_sub(_multone("(= (+ (* (1) (x)) (2)) (-3))", 2), 3), 1), 3), 1), 2))
    print(_eval(_eval(_multone(_eval(_assoc(_comm(_div(_eval("(= (* (-1) (x)) (+ (2) (3)))", 2), 2), 2), 1), 3), 1), 3), 2))
    print(_eval(_multone(_eval(_dist("(= (+ (* (-1) (x)) (* (2) (x))) (+ (-3) (4)))", 1), 2), 1), 2))
    print(_eval(_multone(_eval(_dist("(= (+ (* (-1) (x)) (* (2) (x))) (- (-3) (4)))", 1), 2), 1), 2))
    print(_eval(_addzero(_eval(_assoc(_subsub(_multone(_add("(= (- (* (1) (x)) (2)) (-3))", 5), 3), 2), 1), 3), 1), 2))
    print(_eval(_divself(_assoc(_multone("(= (* (1) (x)) (/ (* (2) (x)) (x)))", 1), 2), 4), 2))
    
    """
    Expected Test Results:
    (= (x) (1))
    (= (x) (-5))
    (= (x) (-5))
    (= (x) (1))
    (= (x) (-7))
    (= (x) (-1))
    (= (x) (2))
    """
    
    #Test that new Lemma primitives are working as expected
    print(_assoc_eval_add0("(- (+ (x) (3)) (3))", 0))
    print(_assoc_eval_eval_add0("(= (- (+ (x) (3)) (3)) (+ (2) (3)))", 0))
    print(_sub_eval_comm("(= (+ (3) (x)) (-4))", 2))
    print(_dist_dist_eval_eval_eval_eval_multone("(= (- (+ (* (3) (x)) (* (3) (x))) (* (5) (x))) (+ (+ (3) (4)) (4)))", 0))
    print(_add_eval_comm_assoc_comm("(= (- (x) (2)) (1))", 3))
    print(_sub_eval_comm_assoc_eval_add0("(= (+ (3) (x)) (-4))", 2))
    print(_add_eval_comm_assoc_comm_assoc_eval_add0("(= (- (* (8) (x)) (9)) (5))", 5))
    print(_sub_assoc_eval_eval_add0("(= (+ (x) (3)) (5))", 3))
    print(_sub_assoc_eval_eval_add0_multone("(= (+ (* (1) (x)) (3)) (5))", 5))
    print(_sub_subsub_comm_assoc_eval_eval_add0_multone("(= (- (3) (x)) (5))", 2))
    print(_div_eval_comm_assoc_eval_multone("(= (* (8) (x)) (14))", 2))
    print(_div_comm_assoc_eval("(= (* (3) (x)) (2))", 2))
    print(_div_comm_assoc_eval_eval_multone("(= (* (3) (x)) (6))", 2))
    print(_sub_dist_comm_assoc_subself_eval("(= (* (5) (x)) (+ (* (2) (x)) (4)))", 5))
    print(_eval_eval("(+ (- (3) (0)) (-7))", 0))
    
    """
    Expected Test Results:
    (x)
    (= (x) (5))
    (= (- (+ (x) (3)) (3)) (-7))
    (= (x) (11))
    (= (- (+ (x) (2)) (2)) (3))
    (= (x) (-7))
    (= (* (8) (x)) (14))
    (= (x) (2))
    (= (x) (2))
    (= (* (- (0) (x)) (1)) (2))
    (= (x) (/ (7) (4)))
    (= (* (x) (1)) (/ (2) (3)))
    (= (x) (2))
    (= (* (3) (x)) (+ (4) (0)))
    (-4)
    """