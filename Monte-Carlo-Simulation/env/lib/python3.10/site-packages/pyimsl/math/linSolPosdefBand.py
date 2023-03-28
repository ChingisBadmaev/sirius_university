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

IMSL_FACTOR = 10004
IMSL_CONDITION = 10270
IMSL_FACTOR_ONLY = 10006
IMSL_SOLVE_ONLY = 10007
# Hand edited this value.
IMSL_FACTOR_USER = 10151
imslmath = loadimsl(MATH)


def linSolPosdefBand(a, ncoda, b, factor=None, condition=None, factorOnly=None, solveOnly=None):
    """ Solves a real symmetric positive definite system of linear equations Ax = b in band symmetric storage mode. Using optional arguments, any of several related computations can be performed. These extra tasks include computing the RTR Cholesky factorization of A, computing the solution of Ax = b given the Cholesky factorization of A, or estimating the L1 condition number of A.
    """
    imslmath.imsl_d_lin_sol_posdef_band.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_lin_sol_posdef_band('
    evalstring += 'c_int(n)'
    evalstring += ','
    # with soveOnly argument a is ignored
    if solveOnly:
        evalstring += 'c_void_p()'
    else:
        a = toNumpyArray(a, 'a', shape=shape, dtype='double',
                         expectedShape=(0, 0))
        evalstring += 'a.ctypes.data_as(c_void_p)'
        n = shape[1]
    evalstring += ','
    evalstring += 'c_int(ncoda)'
    evalstring += ','
    if factorOnly:
        evalstring += 'c_void_p()'
    else:
        b = toNumpyArray(b, 'b', shape=shape,
                         dtype='double', expectedShape=(0))
        evalstring += 'b.ctypes.data_as(c_void_p)'
        n = shape[0]
    if not (factor is None):
        if solveOnly:  # must use IMSL_FACTOR_USER as is input (and output?)
            evalstring += ','
            evalstring += repr(IMSL_FACTOR_USER)
            factor_pFactor_tmp = toNumpyArray(
                factor, 'factor', shape=shape, dtype='double', expectedShape=(ncoda + 1, n))
            evalstring += ','
            evalstring += 'factor_pFactor_tmp.ctypes.data_as(c_void_p)'
        else:  # is an normal output var
            evalstring += ','
            evalstring += repr(IMSL_FACTOR)
            checkForList(factor, 'factor')
            evalstring += ','
            factor_pFactor_tmp = POINTER(c_double)(c_double())
            evalstring += 'byref(factor_pFactor_tmp)'
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
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (factor is None):
        if isinstance(factor, list):
            factor[:] = []
        processRet(factor_pFactor_tmp, shape=(ncoda + 1, n), pyvar=factor)
    if not (condition is None):
        processRet(condition_cond_tmp, shape=1, pyvar=condition)
    return processRet(result, shape=(n), result=True)
