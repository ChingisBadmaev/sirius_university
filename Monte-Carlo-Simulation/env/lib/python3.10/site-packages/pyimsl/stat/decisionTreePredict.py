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

IMSLS_N_SURROGATES = 50920
IMSLS_WEIGHTS = 15400
IMSLS_X_RESPONSE_COL = 40410
IMSLS_X_NODE_IDS = 50930
IMSLS_ERROR_SS = 40174
imslstat = loadimsl(STAT)


def decisionTreePredict(x, varType, tree, nSurrogates=None, weights=None, xResponseCol=None, xNodeIds=None, errorSs=None):
    """ Computes predicted values using a decision tree.
    """
    imslstat.imsls_d_decision_tree_predict.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_decision_tree_predict('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nCols)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    n = shape[0]
    nCols = shape[1]
    evalstring += ','
    varType = toNumpyArray(varType, 'varType', shape=shape,
                           dtype='int', expectedShape=(nCols))
    evalstring += 'varType.ctypes.data_as(c_void_p)'
    evalstring += ','
    # tree = toNumpyArray(tree, 'tree', shape=shape, dtype='struct', expectedShape=(1))
    # evalstring +='tree.ctypes.data_as(c_void_p)'
    evalstring += 'tree'
    if not (nSurrogates is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_SURROGATES)
        evalstring += ','
        evalstring += 'c_int(nSurrogates)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(n))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (xResponseCol is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_RESPONSE_COL)
        evalstring += ','
        evalstring += 'c_int(xResponseCol)'
    if not (xNodeIds is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_NODE_IDS)
        checkForList(xNodeIds, 'xNodeIds')
        evalstring += ','
        xNodeIds_nodeIds_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xNodeIds_nodeIds_tmp)'
    if not (errorSs is None):
        evalstring += ','
        evalstring += repr(IMSLS_ERROR_SS)
        checkForList(errorSs, 'errorSs')
        evalstring += ','
        errorSs_predErrSs_tmp = c_double()
        evalstring += 'byref(errorSs_predErrSs_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (xNodeIds is None):
        processRet(xNodeIds_nodeIds_tmp, shape=(n), pyvar=xNodeIds)
    if not (errorSs is None):
        processRet(errorSs_predErrSs_tmp, shape=(1), pyvar=errorSs)
    return processRet(result, shape=(n), result=True)
