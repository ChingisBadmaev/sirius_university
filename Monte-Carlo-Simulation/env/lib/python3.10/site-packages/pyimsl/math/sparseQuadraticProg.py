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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *
from .mathStructs import Imsl_d_sparse_elem

IMSL_CONSTR_TYPE = 10122
IMSL_UPPER_LIMIT = 10121
IMSL_LOWER_BOUND = 10123
IMSL_UPPER_BOUND = 10124
IMSL_OBJ_CONSTANT = 15088
IMSL_PREORDERING = 15108
IMSL_MAX_ITERATIONS = 15089
IMSL_OPT_TOL = 15090
IMSL_PRINF_TOL = 15096
IMSL_DLINF_TOL = 15097
IMSL_PRINT = 10251
IMSL_PRESOLVE = 15087
IMSL_CSC_FORMAT = 11107
IMSL_TERMINATION_STATUS = 15095
IMSL_OBJ = 10125
IMSL_ITERATION_COUNT = 15010
IMSL_DUAL = 10127
IMSL_PRIMAL_INFEAS = 15091
IMSL_DUAL_INFEAS = 15092
IMSL_CP_RATIO_SMALLEST = 15093
IMSL_CP_RATIO_LARGEST = 15094
imslmath = loadimsl(MATH)


def sparseQuadraticProg(a, b, c, q, constrType=None, upperLimit=None, lowerBound=None, upperBound=None, objConstant=None, preordering=None, maxIterations=None, optTol=None, prinfTol=None, dlinfTol=None, t_print=None, presolve=None, cscFormat=None, terminationStatus=None, obj=None, iterationCount=None, dual=None, primalInfeas=None, dualInfeas=None, cpRatioSmallest=None, cpRatioLargest=None):
    """ Solves a sparse convex quadratic programming problem by an infeasible primal-dual interior-point method.
    """
    imslmath.imsl_d_sparse_quadratic_prog.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_sparse_quadratic_prog('
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nza)'
    evalstring += ','
    evalstring += 'c_int(nzq)'
    evalstring += ','
    # a = toNumpyArray(a, 'a', shape=shape, dtype='struct', expectedShape=(0))
    # evalstring +='a'
    a_tmp = toNumpyArray(a, 'a', shape=shape,
                         dtype='Imsl_d_sparse_elem', expectedShape=(0, 0))
    evalstring += 'a_tmp'
    nza = shape[0]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    m = shape[0]
    evalstring += ','
    c = toNumpyArray(c, 'c', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'c.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    # q = toNumpyArray(q, 'q', shape=shape, dtype='struct', expectedShape=(0))
    # evalstring +='q'
    q_tmp = toNumpyArray(q, 'q', shape=shape,
                         dtype='Imsl_d_sparse_elem', expectedShape=(0, 0))
    evalstring += 'q_tmp'
    nzq = shape[0]
    if not (constrType is None):
        evalstring += ','
        evalstring += repr(IMSL_CONSTR_TYPE)
        evalstring += ','
        constrType = toNumpyArray(
            constrType, 'constrType', shape=shape, dtype='int', expectedShape=(m))
        evalstring += 'constrType.ctypes.data_as(c_void_p)'
    if not (upperLimit is None):
        evalstring += ','
        evalstring += repr(IMSL_UPPER_LIMIT)
        evalstring += ','
        upperLimit = toNumpyArray(
            upperLimit, 'upperLimit', shape=shape, dtype='double', expectedShape=(m))
        evalstring += 'upperLimit.ctypes.data_as(c_void_p)'
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
    if not (objConstant is None):
        evalstring += ','
        evalstring += repr(IMSL_OBJ_CONSTANT)
        evalstring += ','
        evalstring += 'c_double(objConstant)'
    if not (preordering is None):
        evalstring += ','
        evalstring += repr(IMSL_PREORDERING)
        evalstring += ','
        evalstring += 'c_int(preordering)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (optTol is None):
        evalstring += ','
        evalstring += repr(IMSL_OPT_TOL)
        evalstring += ','
        evalstring += 'c_double(optTol)'
    if not (prinfTol is None):
        evalstring += ','
        evalstring += repr(IMSL_PRINF_TOL)
        evalstring += ','
        evalstring += 'c_double(prinfTol)'
    if not (dlinfTol is None):
        evalstring += ','
        evalstring += repr(IMSL_DLINF_TOL)
        evalstring += ','
        evalstring += 'c_double(dlinfTol)'
    if not (t_print is None):
        evalstring += ','
        evalstring += repr(IMSL_PRINT)
        evalstring += ','
        evalstring += 'c_int(t_print)'
    if not (presolve is None):
        evalstring += ','
        evalstring += repr(IMSL_PRESOLVE)
        evalstring += ','
        evalstring += 'c_int(presolve)'
    if not (cscFormat is None):
        evalstring += ','
        evalstring += repr(IMSL_CSC_FORMAT)
        checkForDict(cscFormat, 'cscFormat', [
                     'aColptr', 'aRowind', 'aValues', 'qColptr', 'qRowind', 'qValues'])
        evalstring += ','
        cscFormat_aColptr_tmp = cscFormat['aColptr']
        # cscFormat_aColptr_tmp = toNumpyArray(cscFormat_aColptr_tmp, 'aColptr', shape=shape, dtype='int', expectedShape=(nza))
        cscFormat_aColptr_tmp = toNumpyArray(
            cscFormat_aColptr_tmp, 'aColptr', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'cscFormat_aColptr_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_aRowind_tmp = cscFormat['aRowind']
        # cscFormat_aRowind_tmp = toNumpyArray(cscFormat_aRowind_tmp, 'aRowind', shape=shape, dtype='int', expectedShape=(nza))
        cscFormat_aRowind_tmp = toNumpyArray(
            cscFormat_aRowind_tmp, 'aRowind', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'cscFormat_aRowind_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_aValues_tmp = cscFormat['aValues']
        # cscFormat_aValues_tmp = toNumpyArray(cscFormat_aValues_tmp, 'aValues', shape=shape, dtype='double', expectedShape=(nza))
        cscFormat_aValues_tmp = toNumpyArray(
            cscFormat_aValues_tmp, 'aValues', shape=shape, dtype='double', expectedShape=(0))
        # Need to set nza here since the required argument "a" is ignored when cscFormat is used.
        nza = shape[0]
        evalstring += 'cscFormat_aValues_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_qColptr_tmp = cscFormat['qColptr']
        # cscFormat_qColptr_tmp = toNumpyArray(cscFormat_qColptr_tmp, 'qColptr', shape=shape, dtype='int', expectedShape=(nzq))
        cscFormat_qColptr_tmp = toNumpyArray(
            cscFormat_qColptr_tmp, 'qColptr', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'cscFormat_qColptr_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_qRowind_tmp = cscFormat['qRowind']
        # cscFormat_qRowind_tmp = toNumpyArray(cscFormat_qRowind_tmp, 'qRowind', shape=shape, dtype='int', expectedShape=(nzq))
        cscFormat_qRowind_tmp = toNumpyArray(
            cscFormat_qRowind_tmp, 'qRowind', shape=shape, dtype='int', expectedShape=(0))
        # Need to set nzq here since the required argument "q" is ignored when cscFormat is used.
        nzq = shape[0]
        evalstring += 'cscFormat_qRowind_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_qValues_tmp = cscFormat['qValues']
        # cscFormat_qValues_tmp = toNumpyArray(cscFormat_qValues_tmp, 'qValues', shape=shape, dtype='double', expectedShape=(nzq))
        cscFormat_qValues_tmp = toNumpyArray(
            cscFormat_qValues_tmp, 'qValues', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'cscFormat_qValues_tmp.ctypes.data_as(c_void_p)'
    if not (terminationStatus is None):
        evalstring += ','
        evalstring += repr(IMSL_TERMINATION_STATUS)
        checkForList(terminationStatus, 'terminationStatus')
        evalstring += ','
        terminationStatus_status_tmp = c_int()
        evalstring += 'byref(terminationStatus_status_tmp)'
    if not (obj is None):
        evalstring += ','
        evalstring += repr(IMSL_OBJ)
        checkForList(obj, 'obj')
        evalstring += ','
        obj_obj_tmp = c_double()
        evalstring += 'byref(obj_obj_tmp)'
    if not (iterationCount is None):
        evalstring += ','
        evalstring += repr(IMSL_ITERATION_COUNT)
        checkForList(iterationCount, 'iterationCount')
        evalstring += ','
        iterationCount_iterations_tmp = c_int()
        evalstring += 'byref(iterationCount_iterations_tmp)'
    if not (dual is None):
        evalstring += ','
        evalstring += repr(IMSL_DUAL)
        checkForList(dual, 'dual')
        evalstring += ','
        dual_y_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dual_y_tmp)'
    if not (primalInfeas is None):
        evalstring += ','
        evalstring += repr(IMSL_PRIMAL_INFEAS)
        checkForDict(primalInfeas, 'primalInfeas', [])
        evalstring += ','
        primalInfeas_errB_tmp = c_double()
        evalstring += 'byref(primalInfeas_errB_tmp)'
        evalstring += ','
        primalInfeas_errU_tmp = c_double()
        evalstring += 'byref(primalInfeas_errU_tmp)'
    if not (dualInfeas is None):
        evalstring += ','
        evalstring += repr(IMSL_DUAL_INFEAS)
        checkForList(dualInfeas, 'dualInfeas')
        evalstring += ','
        dualInfeas_errC_tmp = c_double()
        evalstring += 'byref(dualInfeas_errC_tmp)'
    if not (cpRatioSmallest is None):
        evalstring += ','
        evalstring += repr(IMSL_CP_RATIO_SMALLEST)
        checkForList(cpRatioSmallest, 'cpRatioSmallest')
        evalstring += ','
        cpRatioSmallest_cpSmallest_tmp = c_double()
        evalstring += 'byref(cpRatioSmallest_cpSmallest_tmp)'
    if not (cpRatioLargest is None):
        evalstring += ','
        evalstring += repr(IMSL_CP_RATIO_LARGEST)
        checkForList(cpRatioLargest, 'cpRatioLargest')
        evalstring += ','
        cpRatioLargest_cpLargest_tmp = c_double()
        evalstring += 'byref(cpRatioLargest_cpLargest_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (terminationStatus is None):
        processRet(terminationStatus_status_tmp,
                   shape=(1), pyvar=terminationStatus)
    if not (obj is None):
        processRet(obj_obj_tmp, shape=(1), pyvar=obj)
    if not (iterationCount is None):
        processRet(iterationCount_iterations_tmp,
                   shape=(1), pyvar=iterationCount)
    if not (dual is None):
        processRet(dual_y_tmp, shape=(m), pyvar=dual)
    if not (primalInfeas is None):
        processRet(primalInfeas_errB_tmp, shape=(
            1), key='errB', pyvar=primalInfeas)
        processRet(primalInfeas_errU_tmp, shape=(
            1), key='errU', pyvar=primalInfeas)
    if not (dualInfeas is None):
        processRet(dualInfeas_errC_tmp, shape=(1), pyvar=dualInfeas)
    if not (cpRatioSmallest is None):
        processRet(cpRatioSmallest_cpSmallest_tmp,
                   shape=(1), pyvar=cpRatioSmallest)
    if not (cpRatioLargest is None):
        processRet(cpRatioLargest_cpLargest_tmp,
                   shape=(1), pyvar=cpRatioLargest)
    return processRet(result, shape=(n), result=True)
