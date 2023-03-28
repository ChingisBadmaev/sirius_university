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
from numpy import double, dtype, shape, var
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_FACTOR_USER = 10151
IMSL_INVERSE = 10152
IMSL_CONDITION = 10270
IMSL_FACTOR = 10004
IMSL_FACTOR_ONLY = 10006
IMSL_SOLVE_ONLY = 10007
IMSL_INVERSE_ONLY = 10155
imslmath = loadimsl(MATH)


def linSolPosdef(a, b, factor=None, inverse=None, condition=None, factorOnly=None, solveOnly=None, inverseOnly=None):
    """ Solves a real symmetric positive definite system of linear equations Ax = b. Using optional arguments, any of several related computations can be performed. These extra tasks include computing the Cholesky factor, L, of A such that A = LLT, computing the inverse matrix A-1, or computing the solution of Ax = b given the Cholesky factor, L.
    """
    imslmath.imsl_d_lin_sol_posdef.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_lin_sol_posdef('
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    # Ignore param 2 if either of these flags set
    if inverseOnly or factorOnly:
        evalstring += 'c_void_p()'
    else:
        b = toNumpyArray(b, 'b', shape=shape,
                         dtype='double', expectedShape=(n))
        evalstring += 'b.ctypes.data_as(c_void_p)'
    if not (factor is None):
        if solveOnly:  # must use IMSL_FACTOR_USER as is input (and output?)
            evalstring += ','
            evalstring += repr(IMSL_FACTOR_USER)
            factor_pFactor_tmp = toNumpyArray(
                factor, 'factor', shape=shape, dtype='double', expectedShape=(n, n))
            evalstring += ','
            evalstring += 'factor_pFactor_tmp.ctypes.data_as(c_void_p)'
        else:  # is an normal output var
            evalstring += ','
            evalstring += repr(IMSL_FACTOR)
            checkForList(factor, 'factor')
            evalstring += ','
            factor_pFactor_tmp = POINTER(c_double)(c_double())
            evalstring += 'byref(factor_pFactor_tmp)'
    if not (inverse is None):
        evalstring += ','
        evalstring += repr(IMSL_INVERSE)
        checkForList(inverse, 'inverse')
        evalstring += ','
        inverse_pInva_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(inverse_pInva_tmp)'
    if not (condition is None):
        evalstring += ','
        evalstring += repr(IMSL_CONDITION)
        checkForList(condition, 'condition')
        evalstring += ','
        condition_cond_tmp = c_double()
        evalstring += 'byref(condition_cond_tmp)'
    checkForBoolean(factorOnly, 'factorOnly')
    if (factorOnly):
        evalstring += ','
        evalstring += repr(IMSL_FACTOR_ONLY)
    checkForBoolean(solveOnly, 'solveOnly')
    if (solveOnly):
        evalstring += ','
        evalstring += repr(IMSL_SOLVE_ONLY)
    checkForBoolean(inverseOnly, 'inverseOnly')
    if (inverseOnly):
        evalstring += ','
        evalstring += repr(IMSL_INVERSE_ONLY)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (factor is None):
        if isinstance(factor, list):
            factor[:] = []
        processRet(factor_pFactor_tmp, shape=(n, n), pyvar=factor)
    if not (inverse is None):
        processRet(inverse_pInva_tmp, shape=(n, n), pyvar=inverse)
    if not (condition is None):
        processRet(condition_cond_tmp, shape=1, pyvar=condition)
    return processRet(result, shape=(n), result=True)
