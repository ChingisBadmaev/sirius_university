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
from .statStructs import Imsls_d_decision_tree

IMSLS_METHOD = 13170
IMSLS_CRITERIA = 50915
IMSLS_RATIO = 40032
IMSLS_WEIGHTS = 15400
IMSLS_COST_MATRIX = 50917
IMSLS_CONTROL = 50916
IMSLS_COMPLEXITY = 50928
IMSLS_N_SURROGATES = 50920
IMSLS_ALPHAS = 50918
IMSLS_PRIORS = 50919
IMSLS_N_FOLDS = 50921
IMSLS_N_SAMPLE = 13470
IMSLS_TOLERANCE = 15040
IMSLS_RANDOM_SEED = 50600
IMSLS_PRINT = 13900
IMSLS_TEST_DATA = 50926
IMSLS_TEST_DATA_WEIGHTS = 50927
IMSLS_ERROR_SS = 40174
IMSLS_PREDICTED = 16079
imslstat = loadimsl(STAT)


def decisionTree(xy, responseColIdx, varType, method=None, criteria=None, ratio=None, weights=None, costMatrix=None, control=None, complexity=None, nSurrogates=None, alphas=None, priors=None, nFolds=None, nSample=None, tolerance=None, randomSeed=None, printLevel=None, testData=None, testDataWeights=None, errorSs=None, predicted=None):
    """ Generates a decision tree for a single response variable and two or more predictor variables.
    """
    # imslstat.imsls_d_decision_tree.restype = struct
    imslstat.imsls_d_decision_tree.restype = POINTER(Imsls_d_decision_tree)
    shape = []
    evalstring = 'imslstat.imsls_d_decision_tree('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nCols)'
    evalstring += ','
    xy = toNumpyArray(xy, 'xy', shape=shape,
                      dtype='double', expectedShape=(0, 0))
    evalstring += 'xy.ctypes.data_as(c_void_p)'
    n = shape[0]
    nCols = shape[1]
    evalstring += ','
    evalstring += 'c_int(responseColIdx)'
    evalstring += ','
    varType = toNumpyArray(varType, 'varType', shape=shape,
                           dtype='int', expectedShape=(nCols))
    evalstring += 'varType.ctypes.data_as(c_void_p)'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (criteria is None):
        evalstring += ','
        evalstring += repr(IMSLS_CRITERIA)
        evalstring += ','
        evalstring += 'c_int(criteria)'
    checkForBoolean(ratio, 'ratio')
    if (ratio):
        evalstring += ','
        evalstring += repr(IMSLS_RATIO)
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(n))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (costMatrix is None):
        evalstring += ','
        evalstring += repr(IMSLS_COST_MATRIX)
        evalstring += ','
        evalstring += 'c_int(costMatrix_nClasses_tmp)'
        evalstring += ','
        costMatrix_costMatrix_tmp = toNumpyArray(
            costMatrix, 'costMatrix', shape=shape, dtype='double', expectedShape=(0, 0))
        evalstring += 'costMatrix_costMatrix_tmp.ctypes.data_as(c_void_p)'
        costMatrix_nClasses_tmp = shape[0]
    if not (control is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONTROL)
        evalstring += ','
        control = toNumpyArray(
            control, 'control', shape=shape, dtype='int', expectedShape=(5))
        evalstring += 'control.ctypes.data_as(c_void_p)'
    if not (complexity is None):
        evalstring += ','
        evalstring += repr(IMSLS_COMPLEXITY)
        evalstring += ','
        evalstring += 'c_double(complexity)'
    if not (nSurrogates is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_SURROGATES)
        evalstring += ','
        evalstring += 'c_int(nSurrogates)'
    if not (alphas is None):
        evalstring += ','
        evalstring += repr(IMSLS_ALPHAS)
        evalstring += ','
        alphas = toNumpyArray(alphas, 'alphas', shape=shape,
                              dtype='double', expectedShape=(3))
        evalstring += 'alphas.ctypes.data_as(c_void_p)'
    if not (priors is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRIORS)
        evalstring += ','
        evalstring += 'c_int(priors_nClasses_tmp)'
        evalstring += ','
        priors_priors_tmp = toNumpyArray(
            priors, 'priors', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'priors_priors_tmp.ctypes.data_as(c_void_p)'
        priors_nClasses_tmp = shape[0]
    if not (nFolds is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_FOLDS)
        evalstring += ','
        evalstring += 'c_int(nFolds)'
    if not (nSample is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_SAMPLE)
        evalstring += ','
        evalstring += 'c_int(nSample)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (randomSeed is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANDOM_SEED)
        evalstring += ','
        evalstring += 'c_int(randomSeed)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (testData is None):
        evalstring += ','
        evalstring += repr(IMSLS_TEST_DATA)
        evalstring += ','
        evalstring += 'c_int(testData_nTest_tmp)'
        evalstring += ','
        testData_xyTest_tmp = toNumpyArray(
            testData, 'testData', shape=shape, dtype='double', expectedShape=(0, nCols))
        evalstring += 'testData_xyTest_tmp.ctypes.data_as(c_void_p)'
        testData_nTest_tmp = shape[0]
    if not (testDataWeights is None):
        evalstring += ','
        evalstring += repr(IMSLS_TEST_DATA_WEIGHTS)
        evalstring += ','
        testDataWeights = toNumpyArray(testDataWeights, 'testDataWeights',
                                       shape=shape, dtype='double', expectedShape=(testData_nTest_tmp))
        evalstring += 'testDataWeights.ctypes.data_as(c_void_p)'
    if not (errorSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_ERROR_SS)
        checkForList(errorSs, 'errorSs')
        evalstring += ','
        errorSs_predErrSs_tmp = c_double()
        evalstring += 'byref(errorSs_predErrSs_tmp)'
    if not (predicted is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDICTED)
        checkForList(predicted, 'predicted')
        evalstring += ','
        predicted_predicted_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(predicted_predicted_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (errorSs is None):
        processRet(errorSs_predErrSs_tmp, shape=(1), pyvar=errorSs)
    if not (predicted is None):
        processRet(predicted_predicted_tmp, shape=(n), pyvar=predicted)
    # return processRet (result, shape=(1), result=True)
    return result
