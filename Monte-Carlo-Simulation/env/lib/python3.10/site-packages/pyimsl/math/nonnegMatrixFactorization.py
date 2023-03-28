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

IMSL_WEIGHT = 10033
IMSL_INITIAL_FACTORS = 15046
IMSL_ITMAX = 10016
IMSL_RESIDUAL_ERROR = 15047
IMSL_RELATIVE_ERROR = 11138
IMSL_STOPPING_CRITERION = 12002
IMSL_NSTEPS_TAKEN = 14028
imslmath = loadimsl(MATH)


def nonnegMatrixFactorization(a, f, g, weight=None, initialFactors=None, itmax=None, residualError=None, relativeError=None, stoppingCriterion=None, nstepsTaken=None):
    """ Given an m by n real matrix A >= 0, and an integer k<+(min(m,n), compute a factorization A ~= FG.
    """
    imslmath.imsl_d_nonneg_matrix_factorization.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_nonneg_matrix_factorization('
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(k)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    m = shape[0]
    n = shape[1]
    evalstring += ','
    f_tmp = toNumpyArray(f, 'f', shape=shape,
                         dtype='double', expectedShape=(m, 0))
    evalstring += 'f_tmp.ctypes.data_as(c_void_p)'
    k = shape[1]
    evalstring += ','
    # g_tmp = POINTER(c_double)(c_double())
    # evalstring += 'byref(g_tmp)'
    g_tmp = toNumpyArray(g, 'g', shape=shape,
                         dtype='double', expectedShape=(k, n))
    evalstring += 'g_tmp.ctypes.data_as(c_void_p)'
    if not (weight is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHT)
        evalstring += ','
        weight = toNumpyArray(weight, 'weight', shape=shape,
                              dtype='double', expectedShape=(m, n))
        evalstring += 'weight.ctypes.data_as(c_void_p)'
    if not (initialFactors is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_FACTORS)
        evalstring += ','
        evalstring += 'c_int(initialFactors)'
    if not (itmax is None):
        evalstring += ','
        evalstring += repr(IMSL_ITMAX)
        evalstring += ','
        evalstring += 'c_int(itmax)'
    if not (residualError is None):
        evalstring += ','
        evalstring += repr(IMSL_RESIDUAL_ERROR)
        evalstring += ','
        evalstring += 'c_double(residualError)'
    if not (relativeError is None):
        evalstring += ','
        evalstring += repr(IMSL_RELATIVE_ERROR)
        evalstring += ','
        evalstring += 'c_double(relativeError)'
    if not (stoppingCriterion is None):
        evalstring += ','
        evalstring += repr(IMSL_STOPPING_CRITERION)
        checkForList(stoppingCriterion, 'stoppingCriterion')
        evalstring += ','
        stoppingCriterion_reason_tmp = c_int()
        evalstring += 'byref(stoppingCriterion_reason_tmp)'
    if not (nstepsTaken is None):
        evalstring += ','
        evalstring += repr(IMSL_NSTEPS_TAKEN)
        checkForList(nstepsTaken, 'nstepsTaken')
        evalstring += ','
        nstepsTaken_nsteps_tmp = c_int()
        evalstring += 'byref(nstepsTaken_nsteps_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(f_tmp, inout=True, shape=(m, k), pyvar=f)
    # processRet(g_tmp, shape=(k,n), pyvar=g)
    processRet(g_tmp, inout=True, shape=(k, n), pyvar=g)
    if not (stoppingCriterion is None):
        processRet(stoppingCriterion_reason_tmp,
                   shape=(1), pyvar=stoppingCriterion)
    if not (nstepsTaken is None):
        processRet(nstepsTaken_nsteps_tmp, shape=(1), pyvar=nstepsTaken)
    return result
