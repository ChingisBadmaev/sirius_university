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

IMSL_ITMAX = 10016
IMSL_DROP_MAX_POS_DUAL = 15041
IMSL_DROP_TOLERANCE = 11101
IMSL_SUPPLY_WORK_ARRAYS = 15102
IMSL_OPTIMIZED = 15048
IMSL_DUAL_SOLUTION = 15043
IMSL_RESIDUAL_NORM = 11122
imslmath = loadimsl(MATH)


def nonnegLeastSquares(a, b, itmax=None, dropMaxPosDual=None, dropTolerance=None, supplyWorkArrays=None, optimized=None, dualSolution=None, residualNorm=None):
    """ Compute the non-negatice least squares (NNLS) solution of an m by n real linear least squares system, Ax~=b, x>=0.
    """
    imslmath.imsl_d_nonneg_least_squares.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_nonneg_least_squares('
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
    if not (itmax is None):
        evalstring += ','
        evalstring += repr(IMSL_ITMAX)
        evalstring += ','
        evalstring += 'c_int(itmax)'
    if not (dropMaxPosDual is None):
        evalstring += ','
        evalstring += repr(IMSL_DROP_MAX_POS_DUAL)
        evalstring += ','
        evalstring += 'c_int(dropMaxPosDual)'
    if not (dropTolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_DROP_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(dropTolerance)'
    if not (supplyWorkArrays is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_WORK_ARRAYS)
        checkForDict(supplyWorkArrays, 'supplyWorkArrays',
                     ['lwork', 'work', 'liwork', 'iwork'])
        evalstring += ','
        supplyWorkArrays_lwork_tmp = supplyWorkArrays['lwork']
        supplyWorkArrays_lwork_tmp = lwork[0]
        if (not(isinstance(supplyWorkArrays_lwork_tmp, c_int))):
            supplyWorkArrays_lwork_tmp = c_int(lwork[0])
        evalstring += 'byref(supplyWorkArrays_lwork_tmp)'
        evalstring += ','
        supplyWorkArrays_work_tmp = supplyWorkArrays['work']
        supplyWorkArrays_work_tmp = toNumpyArray(
            work, 'work', shape=shape, dtype='double', expectedShape=(supplyWorkArrays_lwork_tmp))
        evalstring += 'supplyWorkArrays_work_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        supplyWorkArrays_liwork_tmp = supplyWorkArrays['liwork']
        supplyWorkArrays_liwork_tmp = liwork[0]
        if (not(isinstance(supplyWorkArrays_liwork_tmp, c_int))):
            supplyWorkArrays_liwork_tmp = c_int(liwork[0])
        evalstring += 'byref(supplyWorkArrays_liwork_tmp)'
        evalstring += ','
        supplyWorkArrays_iwork_tmp = supplyWorkArrays['iwork']
        supplyWorkArrays_iwork_tmp = toNumpyArray(
            iwork, 'iwork', shape=shape, dtype='double', expectedShape=(supplyWorkArrays_liwork_tmp))
        evalstring += 'supplyWorkArrays_iwork_tmp.ctypes.data_as(c_void_p)'
    if not (optimized is None):
        evalstring += ','
        evalstring += repr(IMSL_OPTIMIZED)
        checkForList(optimized, 'optimized')
        evalstring += ','
        optimized_flag_tmp = c_int()
        evalstring += 'byref(optimized_flag_tmp)'
    if not (dualSolution is None):
        evalstring += ','
        evalstring += repr(IMSL_DUAL_SOLUTION)
        checkForList(dualSolution, 'dualSolution')
        evalstring += ','
        dualSolution_dual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dualSolution_dual_tmp)'
    if not (residualNorm is None):
        evalstring += ','
        evalstring += repr(IMSL_RESIDUAL_NORM)
        checkForList(residualNorm, 'residualNorm')
        evalstring += ','
        residualNorm_rnorm_tmp = c_double()
        evalstring += 'byref(residualNorm_rnorm_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (supplyWorkArrays is None):
        processRet(supplyWorkArrays_lwork_tmp, shape=(
            1), key='lwork', inout=True, pyvar=supplyWorkArrays)
        processRet(supplyWorkArrays_work_tmp, shape=(
            supplyWorkArrays_lwork_tmp), key='work', inout=True, pyvar=supplyWorkArrays)
        processRet(supplyWorkArrays_liwork_tmp, shape=(
            1), key='liwork', inout=True, pyvar=supplyWorkArrays)
        processRet(supplyWorkArrays_iwork_tmp, shape=(
            supplyWorkArrays_liwork_tmp), key='iwork', inout=True, pyvar=supplyWorkArrays)
    if not (optimized is None):
        processRet(optimized_flag_tmp, shape=(1), pyvar=optimized)
    if not (dualSolution is None):
        processRet(dualSolution_dual_tmp, shape=(n), pyvar=dualSolution)
    if not (residualNorm is None):
        processRet(residualNorm_rnorm_tmp, shape=(1), pyvar=residualNorm)
    return processRet(result, shape=(n), result=True)
