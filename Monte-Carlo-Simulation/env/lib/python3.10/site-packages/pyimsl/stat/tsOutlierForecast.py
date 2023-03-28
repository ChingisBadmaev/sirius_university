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

IMSLS_CONFIDENCE = 10860
IMSLS_OUT_FREE_FORECAST = 50300
imslstat = loadimsl(STAT)


def tsOutlierForecast(series, outlierStatistics, omega, delta, model, parameters, nPredict, confidence=None, outFreeForecast=None):
    """ Computes forecasts, their associated probability limits and weights for an outlier contaminated time series whose underlying outlier free series follows a general seasonal or nonseasonal ARMA model.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_ts_outlier_forecast.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_ts_outlier_forecast('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    series = toNumpyArray(series, 'series', shape=shape,
                          dtype='double', expectedShape=(0, 2))
    evalstring += 'series.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    evalstring += 'c_int(numOutliers)'
    evalstring += ','
    outlierStatistics = toNumpyArray(
        outlierStatistics, 'outlierStatistics', shape=shape, dtype='int', expectedShape=(0, 2))
    evalstring += 'outlierStatistics.ctypes.data_as(c_void_p)'
    numOutliers = shape[0]
    evalstring += ','
    omega = toNumpyArray(omega, 'omega', shape=shape,
                         dtype='double', expectedShape=(numOutliers))
    evalstring += 'omega.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_double(delta)'
    evalstring += ','
    model = toNumpyArray(model, 'model', shape=shape,
                         dtype='int', expectedShape=(4))
    evalstring += 'model.ctypes.data_as(c_void_p)'
    evalstring += ','
    parameters = toNumpyArray(parameters, 'parameters', shape=shape,
                              dtype='double', expectedShape=(1 + model[0] + model[1]))
    evalstring += 'parameters.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(nPredict)'
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (outFreeForecast is None):
        evalstring += ','
        evalstring += repr(IMSLS_OUT_FREE_FORECAST)
        checkForList(outFreeForecast, 'outFreeForecast')
        evalstring += ','
        outFreeForecast_outFreeForecast_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(outFreeForecast_outFreeForecast_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (outFreeForecast is None):
        processRet(outFreeForecast_outFreeForecast_tmp,
                   shape=(nPredict, 3), pyvar=outFreeForecast)
    return processRet(result, shape=(nPredict, 3), result=True)
