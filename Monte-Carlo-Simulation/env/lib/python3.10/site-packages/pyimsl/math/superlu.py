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
from .mathStructs import Imsl_d_super_lu_factor

NATURAL = 0
MMD_ATA = 1
MMD_AT_PLUS_A = 2
COLAMD = 3
PERMC = 4

IMSL_EQUILIBRATE = 15075
IMSL_COLUMN_ORDERING_METHOD = 15076
IMSL_COLPERM_VECTOR = 15077
IMSL_TRANSPOSE = 10001
IMSL_ITERATIVE_REFINEMENT = 11100
IMSL_FACTOR_SOLVE = 15084
IMSL_DIAG_PIVOT_THRESH = 15078
IMSL_SYMMETRIC_MODE = 15082
IMSL_PERFORMANCE_TUNING = 15083
IMSL_CSC_FORMAT = 11107
IMSL_SUPPLY_SPARSE_LU_FACTOR = 11098
IMSL_RETURN_SPARSE_LU_FACTOR = 11097
IMSL_CONDITION = 10270
IMSL_PIVOT_GROWTH_FACTOR = 15079
IMSL_FORWARD_ERROR_BOUND = 15080
IMSL_BACKWARD_ERROR = 15081
imslmath = loadimsl(MATH)


def superlu(a, b, equilibrate=None, columnOrderingMethod=None, colpermVector=None, transpose=None, iterativeRefinement=None, factorSolve=None, diagPivotThresh=None, symmetricMode=None, performanceTuning=None, cscFormat=None, supplySparseLuFactor=None, returnSparseLuFactor=None, condition=None, pivotGrowthFactor=None, forwardErrorBound=None, backwardError=None):
    """ Computes the LU factorization of a general sparse matrix by a column method and solves the real sparse linear system of equations Ax = b.
    """
    imslmath.imsl_d_superlu.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_superlu('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nz)'
    evalstring += ','
    # a = toNumpyArray(a, 'a', shape=shape, dtype='struct', expectedShape=(0))
    # evalstring +='a'
    a_tmp = toNumpyArray(a, 'a', shape=shape,
                         dtype='Imsl_d_sparse_elem', expectedShape=(0, 0))
    evalstring += 'a_tmp'
    # nz=shape[0]
    nz = len(a)
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    n = shape[0]
    if not (equilibrate is None):
        evalstring += ','
        evalstring += repr(IMSL_EQUILIBRATE)
        evalstring += ','
        evalstring += 'c_int(equilibrate)'
    if not (columnOrderingMethod is None):
        evalstring += ','
        evalstring += repr(IMSL_COLUMN_ORDERING_METHOD)
        evalstring += ','
        evalstring += 'c_int (columnOrderingMethod)'
    if not (colpermVector is None):
        evalstring += ','
        evalstring += repr(IMSL_COLPERM_VECTOR)
        evalstring += ','
        evalstring += 'c_int(colpermVector)'
    if not (transpose is None):
        evalstring += ','
        evalstring += repr(IMSL_TRANSPOSE)
        evalstring += ','
        evalstring += 'c_int(transpose)'
    if not (iterativeRefinement is None):
        evalstring += ','
        evalstring += repr(IMSL_ITERATIVE_REFINEMENT)
        evalstring += ','
        evalstring += 'c_int(iterativeRefinement)'
    if not (factorSolve is None):
        evalstring += ','
        evalstring += repr(IMSL_FACTOR_SOLVE)
        evalstring += ','
        evalstring += 'c_int(factorSolve)'
    if not (diagPivotThresh is None):
        evalstring += ','
        evalstring += repr(IMSL_DIAG_PIVOT_THRESH)
        evalstring += ','
        evalstring += 'c_double(diagPivotThresh)'
    if not (symmetricMode is None):
        evalstring += ','
        evalstring += repr(IMSL_SYMMETRIC_MODE)
        evalstring += ','
        evalstring += 'c_int(symmetricMode)'
    if not (performanceTuning is None):
        evalstring += ','
        evalstring += repr(IMSL_PERFORMANCE_TUNING)
        evalstring += ','
        evalstring += 'c_int(performanceTuning)'
    if not (cscFormat is None):
        evalstring += ','
        evalstring += repr(IMSL_CSC_FORMAT)
        checkForDict(cscFormat, 'cscFormat', [
                     'hbColPtr', 'hbRowInd', 'hbValues'])
        evalstring += ','
        cscFormat_hbColPtr_tmp = cscFormat['hbColPtr']
        cscFormat_hbColPtr_tmp = toNumpyArray(
            cscFormat_hbColPtr_tmp, 'hbColPtr', shape=shape, dtype='int', expectedShape=(nz))
        evalstring += 'cscFormat_hbColPtr_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_hbRowInd_tmp = cscFormat['hbRowInd']
        cscFormat_hbRowInd_tmp = toNumpyArray(
            cscFormat_hbRowInd_tmp, 'hbRowInd', shape=shape, dtype='int', expectedShape=(nz))
        evalstring += 'cscFormat_hbRowInd_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        cscFormat_hbValues_tmp = cscFormat['hbValues']
        cscFormat_hbValues_tmp = toNumpyArray(
            cscFormat_hbValues_tmp, 'hbValues', shape=shape, dtype='double', expectedShape=(nz))
        evalstring += 'cscFormat_hbValues_tmp.ctypes.data_as(c_void_p)'
    if not (supplySparseLuFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_SPARSE_LU_FACTOR)
        evalstring += ','
        evalstring += 'supplySparseLuFactor'
    if not (returnSparseLuFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_SPARSE_LU_FACTOR)
        checkForList(returnSparseLuFactor, 'returnSparseLuFactor')
        evalstring += ','
        returnSparseLuFactor_luFactorReturned_tmp = (Imsl_d_super_lu_factor)()
        evalstring += 'byref(returnSparseLuFactor_luFactorReturned_tmp)'
    if not (condition is None):
        evalstring += ','
        evalstring += repr(IMSL_CONDITION)
        checkForList(condition, 'condition')
        evalstring += ','
        condition_condition_tmp = c_double()
        evalstring += 'byref(condition_condition_tmp)'
    if not (pivotGrowthFactor is None):
        evalstring += ','
        evalstring += repr(IMSL_PIVOT_GROWTH_FACTOR)
        checkForList(pivotGrowthFactor, 'pivotGrowthFactor')
        evalstring += ','
        pivotGrowthFactor_recipPivotGrowth_tmp = c_double()
        evalstring += 'byref(pivotGrowthFactor_recipPivotGrowth_tmp)'
    if not (forwardErrorBound is None):
        evalstring += ','
        evalstring += repr(IMSL_FORWARD_ERROR_BOUND)
        checkForList(forwardErrorBound, 'forwardErrorBound')
        evalstring += ','
        forwardErrorBound_ferr_tmp = c_double()
        evalstring += 'byref(forwardErrorBound_ferr_tmp)'
    if not (backwardError is None):
        evalstring += ','
        evalstring += repr(IMSL_BACKWARD_ERROR)
        checkForList(backwardError, 'backwardError')
        evalstring += ','
        backwardError_berr_tmp = c_double()
        evalstring += 'byref(backwardError_berr_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (returnSparseLuFactor is None):
        # processRet(returnSparseLuFactor_luFactorReturned_tmp, shape=(1), pyvar=returnSparseLuFactor)
        returnSparseLuFactor[:] = []
        returnSparseLuFactor.append(returnSparseLuFactor_luFactorReturned_tmp)
    if not (condition is None):
        processRet(condition_condition_tmp, shape=(1), pyvar=condition)
    if not (pivotGrowthFactor is None):
        processRet(pivotGrowthFactor_recipPivotGrowth_tmp,
                   shape=(1), pyvar=pivotGrowthFactor)
    if not (forwardErrorBound is None):
        processRet(forwardErrorBound_ferr_tmp,
                   shape=(1), pyvar=forwardErrorBound)
    if not (backwardError is None):
        processRet(backwardError_berr_tmp, shape=(1), pyvar=backwardError)
    # return processRet (result, shape=(custom code n), result=True)
    return processRet(result, shape=(n), result=True)
