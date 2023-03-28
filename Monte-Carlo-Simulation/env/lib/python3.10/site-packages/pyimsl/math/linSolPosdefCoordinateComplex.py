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
from pyimsl.util.imslUtils import Imsl_c_sparse_elem, MATH, checkForBoolean, checkForList, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import Imsl_symbolic_factor
from .mathStructs import Imsl_symbolic_factor
from .mathStructs import Imsl_d_numeric_factor

IMSL_RETURN_SYMBOLIC_FACTOR = 11083
IMSL_SUPPLY_SYMBOLIC_FACTOR = 11085
IMSL_SYMBOLIC_FACTOR_ONLY = 11084
IMSL_RETURN_NUMERIC_FACTOR = 11086
IMSL_SUPPLY_NUMERIC_FACTOR = 11087
IMSL_NUMERIC_FACTOR_ONLY = 11088
IMSL_SOLVE_ONLY = 10007
IMSL_MULTIFRONTAL_FACTORIZATION = 11089
IMSL_SMALLEST_DIAGONAL_ELEMENT = 11090
IMSL_LARGEST_DIAGONAL_ELEMENT = 11091
IMSL_NUM_NONZEROS_IN_FACTOR = 11092
IMSL_CSC_FORMAT = 11107
imslmath = loadimsl(MATH)


def linSolPosdefCoordinateComplex(a, b, returnSymbolicFactor=None, supplySymbolicFactor=None, symbolicFactorOnly=None, returnNumericFactor=None, supplyNumericFactor=None, numericFactorOnly=None, solveOnly=None, multifrontalFactorization=None, smallestDiagonalElement=None, largestDiagonalElement=None, numNonzerosInFactor=None, cscFormat=None):
    """ Solves a sparse Hermitian positive definite system of linear equations Ax = b. Using optional arguments, any of several related computations can be performed. These extra tasks include returning the symbolic factorization of A, returning the numeric factorization of A, and computing the solution of Ax = b given either the symbolic or numeric factorizations.
    """
    imslmath.imsl_z_lin_sol_posdef_coordinate.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_lin_sol_posdef_coordinate('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nz)'
    evalstring += ','
    a_tmp = toNumpyArray(a, 'a', shape=shape,
                         dtype='Imsl_c_sparse_elem', expectedShape=(0, 0))
    evalstring += 'a_tmp'
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='d_complex', expectedShape=(0))
    evalstring += 'b'
    n = shape[0]
    nz = len(a)
    if not (returnSymbolicFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_SYMBOLIC_FACTOR)
        checkForList(returnSymbolicFactor, 'returnSymbolicFactor')
        evalstring += ','
        returnSymbolicFactor_symFactor_tmp = (Imsl_symbolic_factor)()
        evalstring += 'byref(returnSymbolicFactor_symFactor_tmp)'
    if not (supplySymbolicFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_SYMBOLIC_FACTOR)
        evalstring += ','
        evalstring += 'byref(supplySymbolicFactor)'
    checkForBoolean(symbolicFactorOnly, 'symbolicFactorOnly')
    if (symbolicFactorOnly):
        evalstring += ','
        evalstring += repr(IMSL_SYMBOLIC_FACTOR_ONLY)
    if not (returnNumericFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_NUMERIC_FACTOR)
        checkForList(returnNumericFactor, 'returnNumericFactor')
        evalstring += ','
        returnNumericFactor_numFactor_tmp = (Imsl_d_numeric_factor)()
        evalstring += 'byref(returnNumericFactor_numFactor_tmp)'
    if not (supplyNumericFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_NUMERIC_FACTOR)
        evalstring += ','
        evalstring += 'byref(supplyNumericFactor)'
    checkForBoolean(numericFactorOnly, 'numericFactorOnly')
    if (numericFactorOnly):
        evalstring += ','
        evalstring += repr(IMSL_NUMERIC_FACTOR_ONLY)
    checkForBoolean(solveOnly, 'solveOnly')
    if (solveOnly):
        evalstring += ','
        evalstring += repr(IMSL_SOLVE_ONLY)
    checkForBoolean(multifrontalFactorization, 'multifrontalFactorization')
    if (multifrontalFactorization):
        evalstring += ','
        evalstring += repr(IMSL_MULTIFRONTAL_FACTORIZATION)
    if not (smallestDiagonalElement is None):
        evalstring += ','
        evalstring += repr(IMSL_SMALLEST_DIAGONAL_ELEMENT)
        checkForList(smallestDiagonalElement, 'smallestDiagonalElement')
        evalstring += ','
        smallestDiagonalElement_smallElement_tmp = c_double()
        evalstring += 'byref(smallestDiagonalElement_smallElement_tmp)'
    if not (largestDiagonalElement is None):
        evalstring += ','
        evalstring += repr(IMSL_LARGEST_DIAGONAL_ELEMENT)
        checkForList(largestDiagonalElement, 'largestDiagonalElement')
        evalstring += ','
        largestDiagonalElement_largestElement_tmp = c_double()
        evalstring += 'byref(largestDiagonalElement_largestElement_tmp)'
    if not (numNonzerosInFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_NUM_NONZEROS_IN_FACTOR)
        checkForList(numNonzerosInFactor, 'numNonzerosInFactor')
        evalstring += ','
        numNonzerosInFactor_numNonzeros_tmp = c_int()
        evalstring += 'byref(numNonzerosInFactor_numNonzeros_tmp)'
    if not (cscFormat is None):
        evalstring += ','
        evalstring += repr(IMSL_CSC_FORMAT)
        checkForDict(cscFormat, 'cscFormat', ['colPtr', 'rowInd', 'values'])
        evalstring += ','
        cscFormat_colPtr_tmp = cscFormat['colPtr']
        cscFormat_colPtr_tmp = toNumpyArray(
            cscFormat_colPtr_tmp, 'colPtr', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'cscFormat_colPtr_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_rowInd_tmp = cscFormat['rowInd']
        cscFormat_rowInd_tmp = toNumpyArray(
            cscFormat_rowInd_tmp, 'rowInd', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'cscFormat_rowInd_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_values_tmp = cscFormat['values']
        cscFormat_values_tmp = toNumpyArray(
            cscFormat_values_tmp, 'values', shape=shape, dtype='d_complex', expectedShape=(0))
        evalstring += 'cscFormat_values_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (returnSymbolicFactor is None):
        returnSymbolicFactor[:] = []
        returnSymbolicFactor.append(returnSymbolicFactor_symFactor_tmp)
    if not (returnNumericFactor is None):
        returnNumericFactor[:] = []
        returnNumericFactor.append(returnNumericFactor_numFactor_tmp)
    if not (smallestDiagonalElement is None):
        processRet(smallestDiagonalElement_smallElement_tmp,
                   shape=1, pyvar=smallestDiagonalElement)
    if not (largestDiagonalElement is None):
        processRet(largestDiagonalElement_largestElement_tmp,
                   shape=1, pyvar=largestDiagonalElement)
    if not (numNonzerosInFactor is None):
        processRet(numNonzerosInFactor_numNonzeros_tmp,
                   shape=1, pyvar=numNonzerosInFactor)
    return processRet(result, shape=(n), result=True)
