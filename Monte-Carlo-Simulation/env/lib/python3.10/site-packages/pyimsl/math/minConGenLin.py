###########################################################################
# Copyright 2008-2019 Rogue Wave Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
###########################################################################
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, gradient, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_XGUESS = 10100
IMSL_GRADIENT = 10250
IMSL_MAX_FCN = 10103
IMSL_NUMBER_ACTIVE_CONSTRAINTS = 11142
IMSL_ACTIVE_CONSTRAINTS = 11140
IMSL_LAGRANGE_MULTIPLIERS = 11143
IMSL_TOLERANCE = 10053
IMSL_OBJ = 10125
IMSL_FCN_W_DATA = 13101
IMSL_GRADIENT_W_DATA = 13102
imslmath = loadimsl(MATH)


def minConGenLin(fcn, neq, a, b, xlb, xub, xguess=None, gradient=None, maxFcn=None, numberActiveConstraints=None, activeConstraints=None, lagrangeMultipliers=None, tolerance=None, obj=None):
    """ Minimizes a general objective function subject to linear equality/inequality constraints.
    """
    imslmath.imsl_d_min_con_gen_lin.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_min_con_gen_lin('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_void_p, c_int, POINTER(c_double), POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(nvar)'
    evalstring += ','
    evalstring += 'c_int(ncon)'
    evalstring += ','
    evalstring += 'c_int(neq)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    ncon = shape[0]
    nvar = shape[1]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(ncon))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    evalstring += ','
    xlb = toNumpyArray(xlb, 'xlb', shape=shape,
                       dtype='double', expectedShape=(nvar))
    evalstring += 'xlb.ctypes.data_as(c_void_p)'
    evalstring += ','
    xub = toNumpyArray(xub, 'xub', shape=shape,
                       dtype='double', expectedShape=(nvar))
    evalstring += 'xub.ctypes.data_as(c_void_p)'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        xguess = toNumpyArray(xguess, 'xguess', shape=shape,
                              dtype='double', expectedShape=(nvar))
        evalstring += 'xguess.ctypes.data_as(c_void_p)'
    if not (gradient is None):
        evalstring += ','
        evalstring += repr(IMSL_GRADIENT)
        evalstring += ','
        checkForCallable(gradient, 'gradient')
        TMP_GRADIENT_GRADIENT = CFUNCTYPE(
            c_void_p, c_int, POINTER(c_double), POINTER(c_double))
        tmp_gradient_gradient = TMP_GRADIENT_GRADIENT(gradient)
        evalstring += 'tmp_gradient_gradient'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    if not (numberActiveConstraints is None):
        evalstring += ','
        evalstring += repr(IMSL_NUMBER_ACTIVE_CONSTRAINTS)
        checkForList(numberActiveConstraints, 'numberActiveConstraints')
        evalstring += ','
        numberActiveConstraints_nact_tmp = c_int()
        evalstring += 'byref(numberActiveConstraints_nact_tmp)'
    if not (activeConstraints is None):
        evalstring += ','
        evalstring += repr(IMSL_ACTIVE_CONSTRAINTS)
        checkForList(activeConstraints, 'activeConstraints')
        evalstring += ','
        activeConstraints_numberActiveConstraints_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(activeConstraints_numberActiveConstraints_tmp)'
    if not (lagrangeMultipliers is None):
        evalstring += ','
        evalstring += repr(IMSL_LAGRANGE_MULTIPLIERS)
        checkForList(lagrangeMultipliers, 'lagrangeMultipliers')
        evalstring += ','
        lagrangeMultipliers_lagrangeMultipliers_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(lagrangeMultipliers_lagrangeMultipliers_tmp)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (obj is None):
        evalstring += ','
        evalstring += repr(IMSL_OBJ)
        checkForList(obj, 'obj')
        evalstring += ','
        obj_obj_tmp = c_double()
        evalstring += 'byref(obj_obj_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (numberActiveConstraints is None):
        processRet(numberActiveConstraints_nact_tmp,
                   shape=1, pyvar=numberActiveConstraints)
    if not (activeConstraints is None):
        processRet(activeConstraints_numberActiveConstraints_tmp, shape=(
            numberActiveConstraints_nact_tmp), pyvar=activeConstraints)
    if not (lagrangeMultipliers is None):
        processRet(lagrangeMultipliers_lagrangeMultipliers_tmp, shape=(
            numberActiveConstraints_nact_tmp), pyvar=lagrangeMultipliers)
    if not (obj is None):
        processRet(obj_obj_tmp, shape=1, pyvar=obj)
    return processRet(result, shape=(nvar), result=True)
