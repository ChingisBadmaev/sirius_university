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
from numpy import dtype, int, shape, transpose, var
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import d_complex

IMSL_TRANSPOSE = 10001
IMSL_FACTOR = 10004
IMSL_INVERSE = 10152
IMSL_CONDITION = 10270
IMSL_FACTOR_ONLY = 10006
IMSL_SOLVE_ONLY = 10007
IMSL_INVERSE_ONLY = 10155
# Hand edited this value.
IMSL_FACTOR_USER = 10151
imslmath = loadimsl(MATH)


def linSolGenComplex(a, b, transpose=None, factor=None, inverse=None, condition=None, factorOnly=None, solveOnly=None, inverseOnly=None):
    """ Solves a complex general system of linear equations Ax = b. Using optional arguments, any of several related computations can be performed. These extra tasks include computing the LU factorization of A using partial pivoting, computing the inverse matrix A-1, solving AHx = b, or computing the solution of Ax = b given the LU factorization of A.
    """
    imslmath.imsl_z_lin_sol_gen.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_lin_sol_gen('
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='d_complex',
                     expectedShape=(0, 0))
    evalstring += 'a'
    n = shape[0]
    evalstring += ','
    # Ignore param 2 if either of these flags set
    if inverseOnly or factorOnly:
        evalstring += 'c_void_p()'
    else:
        b = toNumpyArray(b, 'b', shape=shape,
                         dtype='d_complex', expectedShape=(n))
        evalstring += 'b'
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
            factor_pFactor_tmp = POINTER(d_complex)(d_complex())
            evalstring += 'byref(factor_pPvt_tmp)'
            evalstring += ','
            evalstring += 'byref(factor_pFactor_tmp)'
    if not (inverse is None):
        evalstring += ','
        evalstring += repr(IMSL_INVERSE)
        checkForList(inverse, 'inverse')
        evalstring += ','
        inverse_pInva_tmp = POINTER(d_complex)(d_complex())
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
        processRet(factor_pPvt_tmp, shape=(n), key='pPvt', pyvar=factor)
        processRet(factor_pFactor_tmp, shape=(
            n, n), key='pFactor', pyvar=factor)
    if not (inverse is None):
        processRet(inverse_pInva_tmp, shape=(n, n), pyvar=inverse)
    if not (condition is None):
        processRet(condition_cond_tmp, shape=1, pyvar=condition)
    return processRet(result, shape=(n), result=True)
