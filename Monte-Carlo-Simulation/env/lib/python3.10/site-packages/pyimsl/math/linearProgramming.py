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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_A_COL_DIM = 10003
IMSL_UPPER_LIMIT = 10121
IMSL_CONSTR_TYPE = 10122
IMSL_LOWER_BOUND = 10123
IMSL_UPPER_BOUND = 10124
IMSL_REFINEMENT = 15012
IMSL_EXTENDED_REFINEMENT = 15013
IMSL_OBJ = 10125
IMSL_DUAL = 10127
imslmath = loadimsl(MATH)


def linearProgramming(a, b, c, aColDim=None, upperLimit=None, constrType=None, lowerBound=None, upperBound=None, refinement=None, extendedRefinement=None, obj=None, dual=None):
    """ Solves a linear programming problem.
    """
    VersionFacade.checkVersion(6)
    imslmath.imsl_d_linear_programming.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_linear_programming('
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    m = shape[0]
    n = shape[1]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(m))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    evalstring += ','
    c = toNumpyArray(c, 'c', shape=shape, dtype='double', expectedShape=(n))
    evalstring += 'c.ctypes.data_as(c_void_p)'
    if not (aColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_A_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(aColDim)'
    if not (upperLimit is None):
        evalstring += ','
        evalstring += repr(IMSL_UPPER_LIMIT)
        evalstring += ','
        upperLimit = toNumpyArray(
            upperLimit, 'upperLimit', shape=shape, dtype='double', expectedShape=(m))
        evalstring += 'upperLimit.ctypes.data_as(c_void_p)'
    if not (constrType is None):
        evalstring += ','
        evalstring += repr(IMSL_CONSTR_TYPE)
        evalstring += ','
        constrType = toNumpyArray(
            constrType, 'constrType', shape=shape, dtype='int', expectedShape=(m))
        evalstring += 'constrType.ctypes.data_as(c_void_p)'
    if not (lowerBound is None):
        evalstring += ','
        evalstring += repr(IMSL_LOWER_BOUND)
        evalstring += ','
        lowerBound = toNumpyArray(
            lowerBound, 'lowerBound', shape=shape, dtype='double', expectedShape=(n))
        evalstring += 'lowerBound.ctypes.data_as(c_void_p)'
    if not (upperBound is None):
        evalstring += ','
        evalstring += repr(IMSL_UPPER_BOUND)
        evalstring += ','
        upperBound = toNumpyArray(
            upperBound, 'upperBound', shape=shape, dtype='double', expectedShape=(n))
        evalstring += 'upperBound.ctypes.data_as(c_void_p)'
    checkForBoolean(refinement, 'refinement')
    if (refinement):
        evalstring += ','
        evalstring += repr(IMSL_REFINEMENT)
    checkForBoolean(extendedRefinement, 'extendedRefinement')
    if (extendedRefinement):
        evalstring += ','
        evalstring += repr(IMSL_EXTENDED_REFINEMENT)
    if not (obj is None):
        evalstring += ','
        evalstring += repr(IMSL_OBJ)
        checkForList(obj, 'obj')
        evalstring += ','
        obj_obj_tmp = c_double()
        evalstring += 'byref(obj_obj_tmp)'
    if not (dual is None):
        evalstring += ','
        evalstring += repr(IMSL_DUAL)
        checkForList(dual, 'dual')
        evalstring += ','
        dual_y_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dual_y_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (obj is None):
        processRet(obj_obj_tmp, shape=1, pyvar=obj)
    if not (dual is None):
        processRet(dual_y_tmp, shape=(m), pyvar=dual)
    return processRet(result, shape=(n), result=True)
