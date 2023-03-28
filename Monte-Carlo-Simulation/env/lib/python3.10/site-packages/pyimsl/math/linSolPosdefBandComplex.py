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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import dtype, shape, var
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex

IMSL_FACTOR = 10004
# Hand edited this value.
IMSL_FACTOR_USER = 10151
IMSL_CONDITION = 10270
IMSL_FACTOR_ONLY = 10006
IMSL_SOLVE_ONLY = 10007
imslmath = loadimsl(MATH)


def linSolPosdefBandComplex(a, ncoda, b, factor=None, condition=None, factorOnly=None, solveOnly=None):
    """ Solves a complex Hermitian positive definite system of linear equations Ax = b in band symmetric storage mode. Using optional arguments, any of several related computations can be performed. These extra tasks include computing the  RHR Cholesky factorization of A, computing the solution of Ax = b given the  Cholesky factorization of A, or estimating the L1 condition number of A.
    """
    imslmath.imsl_z_lin_sol_posdef_band.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_lin_sol_posdef_band('
    evalstring += 'c_int(n)'
    evalstring += ','

    a = toNumpyArray(a, 'a', shape=shape, dtype='d_complex',
                     expectedShape=(0, 0))
    evalstring += 'a'
    n = shape[1]
    evalstring += ','
    evalstring += 'c_int(ncoda)'
    evalstring += ','
    if factorOnly:
        evalstring += 'c_void_p()'
    else:
        b = toNumpyArray(b, 'b', shape=shape,
                         dtype='d_complex', expectedShape=(0))
        evalstring += 'b'
        n = shape[0]
    if not (factor is None):
        if solveOnly:  # must use IMSL_FACTOR_USER as is input (and output?)
            evalstring += ','
            evalstring += repr(IMSL_FACTOR_USER)
            factor_pFactor_tmp = toNumpyArray(
                factor, 'factor', shape=shape, dtype='d_complex', expectedShape=(0, 0))
            evalstring += ','
            evalstring += 'factor_pFactor_tmp'
        else:  # is an normal output var
            evalstring += ','
            evalstring += repr(IMSL_FACTOR)
            checkForList(factor, 'factor')
            evalstring += ','
            factor_pFactor_tmp = POINTER(d_complex)(d_complex())
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
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    # When solveOnly is used factor is input so we so not have to do
    # a process ret.  if we do end up using a processRet, it causes
    # a seg fault because of freeing the memory twice.  The input
    # variables created by ctypes seem to managed(free and malloc)
    # by ctypes.  Memory is not malloced in imslUtils so we cannot free
    # it.
    if not (factor is None) and (solveOnly is None):
        if isinstance(factor, list):
            factor[:] = []
        processRet(factor_pFactor_tmp, shape=(ncoda + 1, n), pyvar=factor)
    if not (condition is None):
        processRet(condition_condition_tmp, shape=1, pyvar=condition)
    return processRet(result, shape=(n), result=True)
