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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, int, shape, size, sum
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_X_COL_DIM = 15470
IMSLS_X_CLASS_COLUMNS = 16030
IMSLS_MODEL_ORDER = 13210
IMSLS_INDICES_EFFECTS = 12300
IMSLS_DUMMY = 11270
IMSLS_REGRESSORS = 16000
IMSLS_REGRESSORS_COL_DIM = 16020
ALL = 1
LEAVE_OUT_LAST = 2
SUM_TO_ZERO = 3
imslstat = loadimsl(STAT)


def regressorsForGlm(x, nClass, nContinuous, xColDim=None, xClassColumns=None, modelOrder=None, indicesEffects=None, dummy=None, regressors=None, regressorsColDim=None):
    """ Generates regressors for a general linear model.
    """
    imslstat.imsls_d_regressors_for_glm.restype = c_int
    shape = []
    evalstring = 'imslstat.imsls_d_regressors_for_glm('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                     expectedShape=(0, nClass + nContinuous))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(nClass)'
    evalstring += ','
    evalstring += 'c_int(nContinuous)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (xClassColumns is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_CLASS_COLUMNS)
        evalstring += ','
        xClassColumns = toNumpyArray(
            xClassColumns, 'xClassColumns', shape=shape, dtype='int', expectedShape=(nClass))
        evalstring += 'xClassColumns.ctypes.data_as(c_void_p)'
    if not (modelOrder is None):
        evalstring += ','
        evalstring += repr(IMSLS_MODEL_ORDER)
        evalstring += ','
        evalstring += 'c_int(modelOrder)'
    if not (indicesEffects is None):
        evalstring += ','
        evalstring += repr(IMSLS_INDICES_EFFECTS)
        checkForDict(indicesEffects, 'indicesEffects',
                     ['nVarEffects', 'indicesEffects'])
        evalstring += ','
        evalstring += 'c_int(indicesEffects_nEffects_tmp)'
        evalstring += ','
        indicesEffects_nVarEffects_tmp = indicesEffects['nVarEffects']
        indicesEffects_nVarEffects_tmp = toNumpyArray(
            indicesEffects_nVarEffects_tmp, 'nVarEffects', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'indicesEffects_nVarEffects_tmp.ctypes.data_as(c_void_p)'
        indicesEffects_nEffects_tmp = shape[0]
        evalstring += ','
        indicesEffects_indicesEffects_tmp = indicesEffects['indicesEffects']
        indicesEffects_indicesEffects_tmp = toNumpyArray(
            indicesEffects_indicesEffects_tmp, 'indicesEffects', shape=shape, dtype='int', expectedShape=sum(indicesEffects_nVarEffects_tmp))
        evalstring += 'indicesEffects_indicesEffects_tmp.ctypes.data_as(c_void_p)'
    if not (dummy is None):
        evalstring += ','
        evalstring += repr(IMSLS_DUMMY)
        evalstring += ','
        evalstring += 'c_int (dummy)'
    if not (regressors is None):
        evalstring += ','
        evalstring += repr(IMSLS_REGRESSORS)
        checkForList(regressors, 'regressors')
        evalstring += ','
        regressors_regressors_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(regressors_regressors_tmp)'
    if not (regressorsColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_REGRESSORS_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(regressorsColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (regressors is None):
        processRet(regressors_regressors_tmp, shape=(
            nObservations, result), pyvar=regressors)
    return result
