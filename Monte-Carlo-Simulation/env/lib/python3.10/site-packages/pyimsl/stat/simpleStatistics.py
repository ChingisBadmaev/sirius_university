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
from pyimsl.util.imslUtils import STAT, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, median, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_CONFIDENCE_MEANS = 10880
IMSLS_CONFIDENCE_VARIANCES = 10910
IMSLS_X_COL_DIM = 15470
IMSLS_STAT_COL_DIM = 14800
IMSLS_MEDIAN = 13150
IMSLS_MEDIAN_AND_SCALE = 13160
IMSLS_MISSING_LISTWISE = 18010
IMSLS_MISSING_ELEMENTWISE = 18011
IMSLS_FREQUENCIES = 11790
IMSLS_WEIGHTS = 15400
IMSLS_IDO = 20440
imslstat = loadimsl(STAT)


def simpleStatistics(x, confidenceMeans=None, confidenceVariances=None, xColDim=None, statColDim=None, median=None, medianAndScale=None, missingListwise=None, missingElementwise=None, frequencies=None, weights=None, ido=None):
    """ Computes basic univariate statistics.
    """
    imslstat.imsls_d_simple_statistics.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_simple_statistics('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    nVariables = shape[1]
    retsize = 14
    if not (confidenceMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE_MEANS)
        evalstring += ','
        evalstring += 'c_double(confidenceMeans)'
    if not (confidenceVariances is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE_VARIANCES)
        evalstring += ','
        evalstring += 'c_double(confidenceVariances)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (statColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_STAT_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(statColDim)'
    checkForBoolean(median, 'median')
    if (median):
        retsize = 15
        evalstring += ','
        evalstring += repr(IMSLS_MEDIAN)
    checkForBoolean(medianAndScale, 'medianAndScale')
    if (medianAndScale):
        retsize = 17
        evalstring += ','
        evalstring += repr(IMSLS_MEDIAN_AND_SCALE)
    checkForBoolean(missingListwise, 'missingListwise')
    if (missingListwise):
        evalstring += ','
        evalstring += repr(IMSLS_MISSING_LISTWISE)
    checkForBoolean(missingElementwise, 'missingElementwise')
    if (missingElementwise):
        evalstring += ','
        evalstring += repr(IMSLS_MISSING_ELEMENTWISE)
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (ido is None):
        evalstring += ','
        evalstring += repr(IMSLS_IDO)
        evalstring += ','
        evalstring += 'c_int(ido)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(retsize, nVariables), result=True)
