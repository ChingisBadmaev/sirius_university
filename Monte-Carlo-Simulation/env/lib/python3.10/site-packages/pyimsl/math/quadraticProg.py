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
from pyimsl.util.imslUtils import MATH, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_A_COL_DIM = 10003
IMSL_H_COL_DIM = 10130
IMSL_DUAL = 10127
IMSL_ADD_TO_DIAG_H = 10131
IMSL_OBJ = 10125
IMSL_MAX_ITN = 10113
IMSL_TOLERANCE = 10053
imslmath = loadimsl(MATH)


def quadraticProg(meq, a, b, g, h, aColDim=None, hColDim=None, dual=None, addToDiagH=None, obj=None, maxItn=None, tolerance=None):
    """ Solves a quadratic programming problem subject to linear equality or inequality constraints.
    """
    imslmath.imsl_d_quadratic_prog.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_quadratic_prog('
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(meq)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    m = shape[0]
    n = shape[1]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(m))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    evalstring += ','
    g = toNumpyArray(g, 'g', shape=shape, dtype='double', expectedShape=(n))
    evalstring += 'g.ctypes.data_as(c_void_p)'
    evalstring += ','
    h = toNumpyArray(h, 'h', shape=shape, dtype='double', expectedShape=(n, n))
    evalstring += 'h.ctypes.data_as(c_void_p)'
    if not (aColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_A_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(aColDim)'
    if not (hColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_H_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(hColDim)'
    if not (dual is None):
        evalstring += ','
        evalstring += repr(IMSL_DUAL)
        checkForList(dual, 'dual')
        evalstring += ','
        dual_dual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dual_dual_tmp)'
    if not (addToDiagH is None):
        evalstring += ','
        evalstring += repr(IMSL_ADD_TO_DIAG_H)
        checkForList(addToDiagH, 'addToDiagH')
        evalstring += ','
        addToDiagH_addToDiagH_tmp = c_double()
        evalstring += 'byref(addToDiagH_addToDiagH_tmp)'
    if not (obj is None):
        evalstring += ','
        evalstring += repr(IMSL_OBJ)
        checkForList(obj, 'obj')
        evalstring += ','
        obj_obj_tmp = c_double()
        evalstring += 'byref(obj_obj_tmp)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (dual is None):
        processRet(dual_dual_tmp, shape=(m), pyvar=dual)
    if not (addToDiagH is None):
        processRet(addToDiagH_addToDiagH_tmp, shape=1, pyvar=addToDiagH)
    if not (obj is None):
        processRet(obj_obj_tmp, shape=1, pyvar=obj)
    return processRet(result, shape=(n), result=True)
