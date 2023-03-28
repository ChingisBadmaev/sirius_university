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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, int, shape, transpose
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_TRANSPOSE = 10001
IMSL_FACTOR = 10004
IMSL_CONDITION = 10270
IMSL_FACTOR_ONLY = 10006
IMSL_SOLVE_ONLY = 10007
IMSL_BLOCKING_FACTOR = 11119
# Hand edited this value.
IMSL_FACTOR_USER = 10151
imslmath = loadimsl(MATH)


def linSolGenBand(a, nlca, nuca, b, transpose=None, factor=None, condition=None, factorOnly=None, solveOnly=None, blockingFactor=None):
    """ Solves a real general band system of linear equations, Ax = b. Using optional arguments, any of several related computations can be performed. These extra tasks include computing  the LU factorization of A using partial pivoting, solving ATx = b, or computing the solution of Ax = b given the LU factorization of A.
    """
    imslmath.imsl_d_lin_sol_gen_band.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_lin_sol_gen_band('
    evalstring += 'c_int(n)'
    evalstring += ','
    # Note that the documentation says that the size of a is
    # (nlca+nuca+1), but it's really (nlca+nuca+1)*n.
    if solveOnly:
        evalstring += 'c_void_p()'
    else:
        a = toNumpyArray(a, 'a', shape=shape, dtype='double',
                         expectedShape=(0, 0))
        evalstring += 'a.ctypes.data_as(c_void_p)'
        n = shape[1]
    evalstring += ','
    evalstring += 'c_int(nlca)'
    evalstring += ','
    evalstring += 'c_int(nuca)'
    evalstring += ','
    if factorOnly:
        evalstring += 'c_void_p()'
    else:
        b = toNumpyArray(b, 'b', shape=shape,
                         dtype='double', expectedShape=(0))
        evalstring += 'b.ctypes.data_as(c_void_p)'
        n = shape[0]
    checkForBoolean(transpose, 'transpose')
    if (transpose):
        evalstring += ','
        evalstring += repr(IMSL_TRANSPOSE)
    if not (factor is None):
        if solveOnly:  # must use IMSL_FACTOR_USER as is input (and output?)
            evalstring += ','
            evalstring += repr(IMSL_FACTOR_USER)
            checkForDict(factor, 'factor', ['pPvt', 'pFactor'])
            evalstring += ','
            pPvt = factor['pPvt']
            factor_pPvt_tmp = toNumpyArray(
                pPvt, 'pPvt', shape=shape, dtype='int', expectedShape=(n))
            evalstring += 'factor_pPvt_tmp.ctypes.data_as(c_void_p)'
            evalstring += ','
            pFactor = factor['pFactor']
            factor_pFactor_tmp = toNumpyArray(
                pFactor, 'pFactor', shape=shape, dtype='double', expectedShape=(n, n))
            evalstring += 'factor_pFactor_tmp.ctypes.data_as(c_void_p)'
        else:
            # is a normal output var
            evalstring += ','
            evalstring += repr(IMSL_FACTOR)
            checkForDict(factor, 'factor', [])
            evalstring += ','
            factor_pPvt_tmp = POINTER(c_int)(c_int())
            factor_pFactor_tmp = POINTER(c_double)(c_double())
            evalstring += 'byref(factor_pPvt_tmp)'
            evalstring += ','
            evalstring += 'byref(factor_pFactor_tmp)'
    if not (condition is None):
        evalstring += ','
        evalstring += repr(IMSL_CONDITION)
        checkForList(condition, 'condition')
        evalstring += ','
        condition_condition_tmp = c_double()
        evalstring += 'byref(condition_condition_tmp)'
    checkForBoolean(factorOnly, 'factorOnly')
    if (factorOnly):
        evalstring += ','
        evalstring += repr(IMSL_FACTOR_ONLY)
    checkForBoolean(solveOnly, 'solveOnly')
    if (solveOnly):
        evalstring += ','
        evalstring += repr(IMSL_SOLVE_ONLY)
    if not (blockingFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_BLOCKING_FACTOR)
        evalstring += ','
        evalstring += 'c_int(blockingFactor)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (factor is None):
        processRet(factor_pPvt_tmp, shape=(n), key='pPvt', pyvar=factor)
        processRet(factor_pFactor_tmp, shape=(
            n, n), key='pFactor', pyvar=factor)
    if not (condition is None):
        processRet(condition_condition_tmp, shape=1, pyvar=condition)
#
# No value is returned by the function if factorOnly is specified.
# Otherwise, the result is an array of size n.
#
    if (not(factorOnly is None)):
        return None
    else:
        return processRet(result, shape=(n), result=True)
