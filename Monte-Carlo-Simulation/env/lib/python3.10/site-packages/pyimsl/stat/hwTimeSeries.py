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

IMSLS_ADDITIVE = 50811
IMSLS_SERIES_INCREMENT = 50808
IMSLS_NONSEASONAL_TREND = 25130
IMSLS_NONSEASONAL_CONSTANT = 25125
IMSLS_USE_PARAMS = 50822
IMSLS_N_SAMPLE = 13470
IMSLS_BOUNDS = 10290
IMSLS_INIT_INPUT = 20750
IMSLS_FORECAST_CONFIDENCE = 25710
IMSLS_FORECASTS = 25730
IMSLS_SERIES_SMOOTHED = 50816
IMSLS_COV = 20310
IMSLS_SS_RESIDUAL = 14740
imslstat = loadimsl(STAT)


def hwTimeSeries(nseason, y, additive=None, seriesIncrement=None, nonseasonalTrend=None, nonseasonalConstant=None, useParams=None, nSample=None, bounds=None, initInput=None, forecastConfidence=None, forecasts=None, seriesSmoothed=None, cov=None, ssResidual=None):
    imslstat.imsls_d_hw_time_series.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_hw_time_series('
    evalstring += 'c_int(nobs)'
    evalstring += ','
    evalstring += 'c_int(nseason)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    nvars_tmp = 3
    nobs = shape[0]
    if not (additive is None):
        evalstring += ','
        evalstring += repr(IMSLS_ADDITIVE)
        evalstring += ','
        evalstring += 'c_int(additive)'
    if not (seriesIncrement is None):
        evalstring += ','
        evalstring += repr(IMSLS_SERIES_INCREMENT)
        evalstring += ','
        evalstring += 'c_int(seriesIncrement)'
    checkForBoolean(nonseasonalTrend, 'nonseasonalTrend')
    if (nonseasonalTrend):
        evalstring += ','
        evalstring += repr(IMSLS_NONSEASONAL_TREND)
        nvars_tmp = 2
    checkForBoolean(nonseasonalConstant, 'nonseasonalConstant')
    if (nonseasonalConstant):
        evalstring += ','
        evalstring += repr(IMSLS_NONSEASONAL_CONSTANT)
        nvars_tmp = 1
    if not (useParams is None):
        evalstring += ','
        evalstring += repr(IMSLS_USE_PARAMS)
        evalstring += ','
        useParams = toNumpyArray(
            useParams, 'useParams', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'useParams.ctypes.data_as(c_void_p)'
    if not (nSample is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_SAMPLE)
        evalstring += ','
        evalstring += 'c_int(nSample)'
    if not (bounds is None):
        evalstring += ','
        evalstring += repr(IMSLS_BOUNDS)
        evalstring += ','
        bounds = toNumpyArray(bounds, 'bounds', shape=shape,
                              dtype='double', expectedShape=(6))
        evalstring += 'bounds.ctypes.data_as(c_void_p)'
    if not (initInput is None):
        evalstring += ','
        evalstring += repr(IMSLS_INIT_INPUT)
        evalstring += ','
        evalstring += 'c_int(initInput)'
    if not (forecastConfidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_FORECAST_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(forecastConfidence)'
    if not (forecasts is None):
        evalstring += ','
        evalstring += repr(IMSLS_FORECASTS)
        checkForDict(forecasts, 'forecasts', ['nforecasts'])
        evalstring += ','
        forecasts_nforecasts_tmp = forecasts['nforecasts']
        evalstring += 'c_int(forecasts_nforecasts_tmp)'
        evalstring += ','
        forecasts_forecasts_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(forecasts_forecasts_tmp)'
    if not (seriesSmoothed is None):
        evalstring += ','
        evalstring += repr(IMSLS_SERIES_SMOOTHED)
        checkForList(seriesSmoothed, 'seriesSmoothed')
        evalstring += ','
        seriesSmoothed_ysmoothed_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(seriesSmoothed_ysmoothed_tmp)'
    if not (cov is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV)
        checkForList(cov, 'cov')
        evalstring += ','
        cov_cov_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(cov_cov_tmp)'
    if not (ssResidual is None):
        evalstring += ','
        evalstring += repr(IMSLS_SS_RESIDUAL)
        checkForList(ssResidual, 'ssResidual')
        evalstring += ','
        ssResidual_sumofsquares_tmp = c_double()
        evalstring += 'byref(ssResidual_sumofsquares_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (forecasts is None):
        if not (forecastConfidence is None):
            processRet(forecasts_forecasts_tmp, shape=(
                forecasts_nforecasts_tmp, 3), key='forecasts', pyvar=forecasts)
        else:
            processRet(forecasts_forecasts_tmp, shape=(
                forecasts_nforecasts_tmp), key='forecasts', pyvar=forecasts)
    if not (seriesSmoothed is None):
        processRet(seriesSmoothed_ysmoothed_tmp,
                   shape=(nobs), pyvar=seriesSmoothed)
    if not (cov is None):
        processRet(cov_cov_tmp, shape=(nvars_tmp, nvars_tmp), pyvar=cov)
    if not (ssResidual is None):
        processRet(ssResidual_sumofsquares_tmp, shape=(1), pyvar=ssResidual)
    return processRet(result, shape=((nobs + 1) * nvars_tmp), result=True)
