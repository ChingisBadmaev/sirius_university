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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, int, shape, size, transpose
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_sparse_elem
from .mathStructs import Imsl_d_sparse_lu_factor

# Values for IMSL_PIVOTING_STRATEGY
IMSL_ROW_MARKOWITZ = 0
IMSL_COLUMN_MARKOWITZ = 1
IMSL_SYMMETRIC_MARKOWITZ = 2

IMSL_RETURN_SPARSE_LU_FACTOR = 11097
IMSL_SUPPLY_SPARSE_LU_FACTOR = 11098
IMSL_FREE_SPARSE_LU_FACTOR = 11108
IMSL_RETURN_SPARSE_LU_IN_COORD = 11109
IMSL_SUPPLY_SPARSE_LU_IN_COORD = 11110
IMSL_FACTOR_ONLY = 10006
IMSL_SOLVE_ONLY = 10007
IMSL_TRANSPOSE = 10001
IMSL_CONDITION = 10270
IMSL_PIVOTING_STRATEGY = 11111
IMSL_NUMBER_OF_SEARCH_ROWS = 11099
IMSL_ITERATIVE_REFINEMENT = 11100
IMSL_DROP_TOLERANCE = 11101
IMSL_HYBRID_FACTORIZATION = 11113
IMSL_STABILITY_FACTOR = 11102
IMSL_GROWTH_FACTOR_LIMIT = 11103
IMSL_GROWTH_FACTOR = 11104
IMSL_SMALLEST_PIVOT = 11105
IMSL_NUM_NONZEROS_IN_FACTOR = 11092
IMSL_CSC_FORMAT = 11107
IMSL_MEMORY_BLOCK_SIZE = 11106
imslmath = loadimsl(MATH)


def linSolGenCoordinate(a, b, returnSparseLuFactor=None, supplySparseLuFactor=None, freeSparseLuFactor=None, returnSparseLuInCoord=None, supplySparseLuInCoord=None, factorOnly=None, solveOnly=None, transpose=None, condition=None, pivotingStrategy=None, numberOfSearchRows=None, iterativeRefinement=None, dropTolerance=None, hybridFactorization=None, stabilityFactor=None, growthFactorLimit=None, growthFactor=None, smallestPivot=None, numNonzerosInFactor=None, cscFormat=None, memoryBlockSize=None):
    """ Solves a sparse system of linear equations Ax = b. Using optional arguments, any of several related computations can be performed. These extra tasks include returning the LU factorization of A computing the solution of Ax = b given an LU factorization setting drop tolerances, and controlling iterative refinement.
    """
    imslmath.imsl_d_lin_sol_gen_coordinate.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_lin_sol_gen_coordinate('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nz)'
    evalstring += ','
    a_tmp = toNumpyArray(a, 'a', shape=shape,
                         dtype='Imsl_d_sparse_elem', expectedShape=(0, 0))
    evalstring += 'a_tmp'
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    n = shape[0]
    nz = len(a)
    if not (returnSparseLuFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_SPARSE_LU_FACTOR)
        checkForList(returnSparseLuFactor, 'returnSparseLuFactor')
        evalstring += ','
        returnSparseLuFactor_luFactor_tmp = (Imsl_d_sparse_lu_factor)()
        evalstring += 'byref(returnSparseLuFactor_luFactor_tmp)'
    if not (supplySparseLuFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_SPARSE_LU_FACTOR)
        evalstring += ','
        evalstring += 'byref(supplySparseLuFactor)'
    checkForBoolean(freeSparseLuFactor, 'freeSparseLuFactor')
    if (freeSparseLuFactor):
        evalstring += ','
        evalstring += repr(IMSL_FREE_SPARSE_LU_FACTOR)
    if not (returnSparseLuInCoord is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_SPARSE_LU_IN_COORD)
        checkForDict(returnSparseLuInCoord, 'returnSparseLuInCoord', [])
        evalstring += ','
        returnSparseLuInCoord_luCoordinate_tmp = POINTER(
            Imsl_d_sparse_elem)(Imsl_d_sparse_elem())
        evalstring += 'byref(returnSparseLuInCoord_luCoordinate_tmp)'
        evalstring += ','
        returnSparseLuInCoord_rowPivots_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(returnSparseLuInCoord_rowPivots_tmp)'
        evalstring += ','
        returnSparseLuInCoord_colPivots_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(returnSparseLuInCoord_colPivots_tmp)'
    if not (supplySparseLuInCoord is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_SPARSE_LU_IN_COORD)
        checkForDict(supplySparseLuInCoord, 'supplySparseLuInCoord', [
                     'luCoordinate', 'rowPivots', 'colPivots'])
        evalstring += ','
        evalstring += 'c_int(supplySparseLuInCoord_finalNz_tmp)'
        evalstring += ','
        supplySparseLuInCoord_luCoordinate_tmp = supplySparseLuInCoord['luCoordinate']
        supplySparseLuInCoord_luCoordinate_tmp = toNumpyArray(
            supplySparseLuInCoord_luCoordinate_tmp, 'luCoordinate', shape=shape, dtype='Imsl_d_sparse_elem', expectedShape=(0, 3))
        evalstring += 'supplySparseLuInCoord_luCoordinate_tmp'
        supplySparseLuInCoord_finalNz_tmp = shape[0]
        evalstring += ','
        supplySparseLuInCoord_rowPivots_tmp = supplySparseLuInCoord['rowPivots']
        supplySparseLuInCoord_rowPivots_tmp = toNumpyArray(
            supplySparseLuInCoord_rowPivots_tmp, 'rowPivots', shape=shape, dtype='int', expectedShape=(n))
        evalstring += 'supplySparseLuInCoord_rowPivots_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        supplySparseLuInCoord_colPivots_tmp = supplySparseLuInCoord['colPivots']
        supplySparseLuInCoord_colPivots_tmp = toNumpyArray(
            supplySparseLuInCoord_colPivots_tmp, 'colPivots', shape=shape, dtype='int', expectedShape=(n))
        evalstring += 'supplySparseLuInCoord_colPivots_tmp.ctypes.data_as(c_void_p)'
    checkForBoolean(factorOnly, 'factorOnly')
    if (factorOnly):
        evalstring += ','
        evalstring += repr(IMSL_FACTOR_ONLY)
    checkForBoolean(solveOnly, 'solveOnly')
    if (solveOnly):
        evalstring += ','
        evalstring += repr(IMSL_SOLVE_ONLY)
    checkForBoolean(transpose, 'transpose')
    if (transpose):
        evalstring += ','
        evalstring += repr(IMSL_TRANSPOSE)
    if not (condition is None):
        evalstring += ','
        evalstring += repr(IMSL_CONDITION)
        checkForList(condition, 'condition')
        evalstring += ','
        condition_condition_tmp = c_double()
        evalstring += 'byref(condition_condition_tmp)'
    if not (pivotingStrategy is None):
        evalstring += ','
        evalstring += repr(IMSL_PIVOTING_STRATEGY)
        evalstring += ','
        evalstring += 'c_int(pivotingStrategy)'
    if not (numberOfSearchRows is None):
        evalstring += ','
        evalstring += repr(IMSL_NUMBER_OF_SEARCH_ROWS)
        evalstring += ','
        evalstring += 'c_int(numberOfSearchRows)'
    checkForBoolean(iterativeRefinement, 'iterativeRefinement')
    if (iterativeRefinement):
        evalstring += ','
        evalstring += repr(IMSL_ITERATIVE_REFINEMENT)
    if not (dropTolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_DROP_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(dropTolerance)'
    if not (hybridFactorization is None):
        evalstring += ','
        evalstring += repr(IMSL_HYBRID_FACTORIZATION)
        checkForList(hybridFactorization, 'hybridFactorization', size=2)
        evalstring += ','
        hybridFactorization_density_tmp = hybridFactorization[0]
        evalstring += 'c_double(hybridFactorization_density_tmp)'
        evalstring += ','
        hybridFactorization_orderBound_tmp = hybridFactorization[1]
        evalstring += 'c_int(hybridFactorization_orderBound_tmp)'
    if not (stabilityFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_STABILITY_FACTOR)
        evalstring += ','
        evalstring += 'c_double(stabilityFactor)'
    if not (growthFactorLimit is None):
        evalstring += ','
        evalstring += repr(IMSL_GROWTH_FACTOR_LIMIT)
        evalstring += ','
        evalstring += 'c_double(growthFactorLimit)'
    if not (growthFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_GROWTH_FACTOR)
        checkForList(growthFactor, 'growthFactor')
        evalstring += ','
        growthFactor_gf_tmp = c_double()
        evalstring += 'byref(growthFactor_gf_tmp)'
    if not (smallestPivot is None):
        evalstring += ','
        evalstring += repr(IMSL_SMALLEST_PIVOT)
        checkForList(smallestPivot, 'smallestPivot')
        evalstring += ','
        smallestPivot_smallPivot_tmp = c_double()
        evalstring += 'byref(smallestPivot_smallPivot_tmp)'
    # Always get numNonzerosInFactor as may need for output calculation
    if not (numNonzerosInFactor is None):
        checkForList(numNonzerosInFactor, 'numNonzerosInFactor')
    evalstring += ','
    evalstring += repr(IMSL_NUM_NONZEROS_IN_FACTOR)
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
            cscFormat_values_tmp, 'values', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'cscFormat_values_tmp.ctypes.data_as(c_void_p)'
    if not (memoryBlockSize is None):
        evalstring += ','
        evalstring += repr(IMSL_MEMORY_BLOCK_SIZE)
        evalstring += ','
        evalstring += 'c_int(memoryBlockSize)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (returnSparseLuFactor is None):
        returnSparseLuFactor[:] = []
        returnSparseLuFactor.append(returnSparseLuFactor_luFactor_tmp)
    if not (returnSparseLuInCoord is None):
        processRet(returnSparseLuInCoord_luCoordinate_tmp, shape=(
            numNonzerosInFactor_numNonzeros_tmp), key='luCoordinate', pyvar=returnSparseLuInCoord)
        processRet(returnSparseLuInCoord_rowPivots_tmp, shape=(
            n), key='rowPivots', pyvar=returnSparseLuInCoord)
        processRet(returnSparseLuInCoord_colPivots_tmp, shape=(
            n), key='colPivots', pyvar=returnSparseLuInCoord)
    if not (condition is None):
        processRet(condition_condition_tmp, shape=1, pyvar=condition)
    if not (growthFactor is None):
        processRet(growthFactor_gf_tmp, shape=1, pyvar=growthFactor)
    if not (smallestPivot is None):
        processRet(smallestPivot_smallPivot_tmp, shape=1, pyvar=smallestPivot)
    if not (numNonzerosInFactor is None):
        processRet(numNonzerosInFactor_numNonzeros_tmp,
                   shape=1, pyvar=numNonzerosInFactor)
    return processRet(result, shape=(n), result=True)
