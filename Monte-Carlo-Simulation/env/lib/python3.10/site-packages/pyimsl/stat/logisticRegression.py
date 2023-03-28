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
from numpy import array, empty, double
from ctypes import *
from .statStructs import Imsls_d_model

IMSLS_GROUP_COUNTS = 12090
IMSLS_GROUPS = 20810
IMSLS_COLUMN_WISE = 50826
IMSLS_FREQUENCIES = 11790
IMSLS_REFERENCE_CLASS = 50828
IMSLS_NO_INTERCEPT = 13350
IMSLS_X_INDICES = 20443
IMSLS_X_INTERACTIONS = 50830
IMSLS_TOLERANCE = 15040
IMSLS_MAX_ITER = 12960
IMSLS_INIT_INPUT = 20750
IMSLS_PREV_RESULTS = 50834
IMSLS_NEXT_RESULTS = 50835
IMSLS_COEFFICIENTS = 50829
IMSLS_LRSTAT = 50885
imslstat = loadimsl(STAT)


def logisticRegression(nIndependent, nClasses, x, y, groupCounts=None, groups=None, columnWise=None, frequencies=None, referenceClass=None, noIntercept=None, xIndices=None, xInteractions=None, tolerance=None, maxIter=None, initInput=None, prevResults=None, nextResults=None, coefficients=None, lrstat=None):
    imslstat.imsls_d_logistic_regression.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_logistic_regression('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    evalstring += 'c_int(nClasses)'
    evalstring += ','
    checkForBoolean(columnWise, 'columnWise')
    if (columnWise):
        x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                         expectedShape=(nIndependent, 0))
        nObservations = shape[1]
    else:
        x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                         expectedShape=(0, nIndependent))
        nObservations = shape[0]
    evalstring += 'x.ctypes.data_as(c_void_p)'
    evalstring += ','
    checkForBoolean(groupCounts, 'groupCounts')
    checkForBoolean(groups, 'groups')
    if (groupCounts):
        y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                         expectedShape=(nObservations, nClasses - 1))
    elif (groups):
        y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                         expectedShape=(nObservations))
    else:
        y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                         expectedShape=(nObservations, nClasses))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    nCoefficients = nIndependent + 1  # custom code
    if (groupCounts):
        evalstring += ','
        evalstring += repr(IMSLS_GROUP_COUNTS)
    if (groups):
        evalstring += ','
        evalstring += repr(IMSLS_GROUPS)
    checkForBoolean(columnWise, 'columnWise')
    if (columnWise):
        evalstring += ','
        evalstring += repr(IMSLS_COLUMN_WISE)
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies_tmp = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'frequencies_tmp.ctypes.data_as(c_void_p)'
    if not (referenceClass is None):
        evalstring += ','
        evalstring += repr(IMSLS_REFERENCE_CLASS)
        evalstring += ','
        evalstring += 'c_int(referenceClass)'
    checkForBoolean(noIntercept, 'noIntercept')
    if (noIntercept):
        evalstring += ','
        evalstring += repr(IMSLS_NO_INTERCEPT)
    if not (xIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INDICES)
        evalstring += ','
        evalstring += 'c_int(xIndices_nXin_tmp)'
        evalstring += ','
        xIndices_xin_tmp = toNumpyArray(
            xIndices, 'xIndices', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'xIndices_xin_tmp.ctypes.data_as(c_void_p)'
        xIndices_nXin_tmp = shape[0]
    if not (xInteractions is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INTERACTIONS)
        evalstring += ','
        evalstring += 'c_int(xInteractions_nXinteract_tmp)'
        evalstring += ','
        xInteractions_xinteract_tmp = toNumpyArray(
            xInteractions, 'xInteractions', shape=shape, dtype='int', expectedShape=(0, 2))
        evalstring += 'xInteractions_xinteract_tmp.ctypes.data_as(c_void_p)'
        xInteractions_nXinteract_tmp = shape[0]
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (maxIter is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITER)
        evalstring += ','
        evalstring += 'c_int(maxIter)'
    if not (initInput is None):
        evalstring += ','
        evalstring += repr(IMSLS_INIT_INPUT)
        evalstring += ','
        evalstring += 'c_int(initInput)'
    if not (prevResults is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREV_RESULTS)
        evalstring += ','
        evalstring += 'byref(prevResults)'
    if not (nextResults is None):
        evalstring += ','
        evalstring += repr(IMSLS_NEXT_RESULTS)
        evalstring += ','
        if isinstance(nextResults, list) and len(nextResults) == 0:
            nextResults_nextModel_tmp = POINTER(Imsls_d_model)()
        else:
            nextResults_nextModel_tmp = POINTER(Imsls_d_model)(nextResults[0])
        evalstring += 'byref(nextResults_nextModel_tmp)'
    if not (coefficients is None):
        evalstring += ','
        evalstring += repr(IMSLS_COEFFICIENTS)
        checkForList(coefficients, 'coefficients')
        evalstring += ','
        coefficients_coefficients_tmp = toNumpyArray(
            coefficients, 'coefficients', shape=shape, dtype='double', expectedShape=(nCoefficients, nClasses))
        evalstring += 'coefficients_coefficients_tmp.ctypes.data_as(c_void_p)'
    if not (lrstat is None):
        evalstring += ','
        evalstring += repr(IMSLS_LRSTAT)
        checkForList(lrstat, 'lrstat')
        evalstring += ','
        lrstat_lrstat_tmp = c_double()
        evalstring += 'byref(lrstat_lrstat_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nextResults is None):
        nextResults[:] = []
        nextResults.append(nextResults_nextModel_tmp[0])
    if not (coefficients is None):
        processRet(coefficients_coefficients_tmp, shape=(
            nCoefficients, nClasses), inout=True, pyvar=coefficients)
    if not (lrstat is None):
        processRet(lrstat_lrstat_tmp, shape=(1), pyvar=lrstat)
    return processRet(result, shape=(nCoefficients, nClasses), result=True)
