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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_METHOD = 13170
IMSLS_MAX_LAG = 25160
IMSLS_NTIMES = 50190
IMSLS_MEAN_ESTIMATE = 16051
IMSLS_CONVERGENCE_TOLERANCE = 10990
IMSLS_RELATIVE_ERROR = 16050
IMSLS_MAX_ITERATIONS = 12970
IMSLS_TIMES_ARRAY = 50470
IMSLS_MISSING_INDEX = 40175
imslstat = loadimsl(STAT)


def estimateMissing(tpoints, z, method=None, maxLag=None, ntimes=None, meanEstimate=None, convergenceTolerance=None, relativeError=None, maxIterations=None, timesArray=None, missingIndex=None):
    """ Estimates missing values in a time series.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_estimate_missing.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_estimate_missing('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    tpoints = toNumpyArray(tpoints, 'tpoints', shape=shape,
                           dtype='int', expectedShape=(0))
    nObs = shape[0]
    evalstring += 'tpoints.ctypes.data_as(c_void_p)'
    evalstring += ','
    z = toNumpyArray(z, 'z', shape=shape, dtype='double', expectedShape=(nObs))
    evalstring += 'z.ctypes.data_as(c_void_p)'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (maxLag is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_LAG)
        evalstring += ','
        evalstring += 'c_int(maxLag)'
    if not (ntimes is None):
        evalstring += ','
        evalstring += repr(IMSLS_NTIMES)
        checkForList(ntimes, 'ntimes')
        evalstring += ','
        ntimes_ntimes_tmp = c_int()
        evalstring += 'byref(ntimes_ntimes_tmp)'
    if not (meanEstimate is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEAN_ESTIMATE)
        evalstring += ','
        evalstring += 'c_int(meanEstimate)'
    if not (convergenceTolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONVERGENCE_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(convergenceTolerance)'
    if not (relativeError is None):
        evalstring += ','
        evalstring += repr(IMSLS_RELATIVE_ERROR)
        evalstring += ','
        evalstring += 'c_double(relativeError)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (timesArray is None):
        evalstring += ','
        evalstring += repr(IMSLS_TIMES_ARRAY)
        checkForList(timesArray, 'timesArray')
        evalstring += ','
        timesArray_timesArray_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(timesArray_timesArray_tmp)'
    if not (missingIndex is None):
        evalstring += ','
        evalstring += repr(IMSLS_MISSING_INDEX)
        checkForList(missingIndex, 'missingIndex')
        evalstring += ','
        missingIndex_missingIndex_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(missingIndex_missingIndex_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (ntimes is None):
        processRet(ntimes_ntimes_tmp, shape=(1), pyvar=ntimes)
    if not (timesArray is None):
        processRet(timesArray_timesArray_tmp, shape=(
            tpoints[nObs - 1] - tpoints[0] + 1), pyvar=timesArray)
    if not (missingIndex is None):
        processRet(missingIndex_missingIndex_tmp, shape=(
            tpoints[nObs - 1] - tpoints[0] + 1 - nObs), pyvar=missingIndex)
    return processRet(result, shape=(tpoints[nObs - 1] - tpoints[0] + 1), result=True)
