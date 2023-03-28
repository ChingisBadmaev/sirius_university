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
from pyimsl.util.imslUtils import MATH, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, median, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSL_CONFIDENCE_MEANS = 10087
IMSL_CONFIDENCE_VARIANCES = 10088
IMSL_X_COL_DIM = 10045
IMSL_STAT_COL_DIM = 10086
IMSL_MEDIAN = 10320
IMSL_MEDIAN_AND_SCALE = 10321
imslmath = loadimsl(MATH)


def simpleStatistics(x, confidenceMeans=None, confidenceVariances=None, xColDim=None, statColDim=None, median=None, medianAndScale=None):
    """ Computes basic univariate statistics.
    """
    imslmath.imsl_d_simple_statistics.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_simple_statistics('
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
        evalstring += repr(IMSL_CONFIDENCE_MEANS)
        evalstring += ','
        evalstring += 'c_double(confidenceMeans)'
    if not (confidenceVariances is None):
        evalstring += ','
        evalstring += repr(IMSL_CONFIDENCE_VARIANCES)
        evalstring += ','
        evalstring += 'c_double(confidenceVariances)'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (statColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_STAT_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(statColDim)'
    checkForBoolean(median, 'median')
    if (median):
        retsize = 15
        evalstring += ','
        evalstring += repr(IMSL_MEDIAN)
    checkForBoolean(medianAndScale, 'medianAndScale')
    if (medianAndScale):
        retsize = 17
        evalstring += ','
        evalstring += repr(IMSL_MEDIAN_AND_SCALE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(retsize, nVariables), result=True)
