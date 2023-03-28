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

MODE_METH = 0
MEAN_METH = 1
MEDIAN_METH = 2
GEOMEAN_METH = 3
LINEAR_METH = 4

IMSLS_MISSING_VALUE = 50847
IMSLS_METRIC_DIAG = 50846
IMSLS_REPLACEMENT_VALUE = 50840
IMSLS_IMPUTE_METHOD = 50842
IMSLS_PURGE = 50843
IMSLS_MISSING_INDEX = 40175
IMSLS_X_IMPUTED = 50844
imslstat = loadimsl(STAT)


def imputeMissing(indind, x, missingValue=None, metricDiag=None, replacementValue=None, imputeMethod=None, purge=None, missingIndex=None, xImputed=None):
    """ Locate and optionally replace dependent variable missing values with nearest neighbor estimates
    """
    imslstat.imsls_d_impute_missing.restype = c_int
    shape = []
    evalstring = 'imslstat.imsls_d_impute_missing('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    indind = toNumpyArray(indind, 'indind', shape=shape,
                          dtype='int', expectedShape=(0))
    evalstring += 'indind.ctypes.data_as(c_void_p)'
    nIndependent = shape[0]
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nVariables = shape[1]
    if not (missingValue is None):
        evalstring += ','
        evalstring += repr(IMSLS_MISSING_VALUE)
        evalstring += ','
        evalstring += 'c_double(missingValue)'
    if not (metricDiag is None):
        evalstring += ','
        evalstring += repr(IMSLS_METRIC_DIAG)
        evalstring += ','
        metricDiag = toNumpyArray(
            metricDiag, 'metricDiag', shape=shape, dtype='double', expectedShape=(nIndependent))
        evalstring += 'metricDiag.ctypes.data_as(c_void_p)'
    if not (replacementValue is None):
        evalstring += ','
        evalstring += repr(IMSLS_REPLACEMENT_VALUE)
        evalstring += ','
        evalstring += 'c_double(replacementValue)'
    if not (imputeMethod is None):
        evalstring += ','
        evalstring += repr(IMSLS_IMPUTE_METHOD)
        checkForDict(imputeMethod, 'imputeMethod', ['method', 'k'])
        evalstring += ','
        imputeMethod_method_tmp = imputeMethod['method']
        evalstring += 'c_int(imputeMethod_method_tmp)'
        evalstring += ','
        imputeMethod_k_tmp = imputeMethod['k']
        evalstring += 'c_int(imputeMethod_k_tmp)'
    if not (purge is None):
        evalstring += ','
        evalstring += repr(IMSLS_PURGE)
        checkForDict(purge, 'purge', [])
        evalstring += ','
        purge_nMissingRows_tmp = c_int()
        evalstring += 'byref(purge_nMissingRows_tmp)'
        evalstring += ','
        purge_missingRowIndices_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(purge_missingRowIndices_tmp)'
    if not (missingIndex is None):
        evalstring += ','
        evalstring += repr(IMSLS_MISSING_INDEX)
        checkForList(missingIndex, 'missingIndex')
        evalstring += ','
        missingIndex_indices_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(missingIndex_indices_tmp)'
    if not (xImputed is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_IMPUTED)
        checkForList(xImputed, 'xImputed')
        evalstring += ','
        xImputed_xImputed_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xImputed_xImputed_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (purge is None):
        processRet(purge_nMissingRows_tmp, shape=(
            1), key='nMissingRows', pyvar=purge)
        processRet(purge_missingRowIndices_tmp, shape=(
            purge_nMissingRows_tmp), key='missingRowIndices', pyvar=purge)
    if not (missingIndex is None):
        processRet(missingIndex_indices_tmp,
                   shape=(result), pyvar=missingIndex)
    if not (xImputed is None):
        if not (purge is None):
            processRet(xImputed_xImputed_tmp, shape=(
                nObservations - purge['nMissingRows'], nVariables), pyvar=xImputed)
        else:
            processRet(xImputed_xImputed_tmp, shape=(
                nObservations, nVariables), pyvar=xImputed)
    return result
