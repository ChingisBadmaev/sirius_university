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

IMSLS_TREND_ORDER = 50935
IMSLS_SEASONAL_ORDER = 50936
IMSLS_NUM_PREDICT = 50440
IMSLS_PERIOD = 50937
IMSLS_SPAN = 50942
IMSLS_RIGIDITY = 50938
IMSLS_MODEL = 20100
IMSLS_PRINT_LEVEL = 20530
IMSLS_NONSEASONAL_TREND = 25130
IMSLS_SEASONAL = 50947
IMSLS_IRREGULAR_COMPONENTS = 50949
IMSLS_SERIES_SMOOTHED = 50816
imslstat = loadimsl(STAT)


def bayesianSeasonalAdj(w, trendOrder=None, seasonalOrder=None, numPredict=None, period=None, span=None, rigidity=None, model=None, printLevel=None, nonseasonalTrend=None, seasonal=None, irregularComponents=None, seriesSmoothed=None):
    """ Decomposes a time series into trend, seasonal, and an error component.
    """
    imslstat.imsls_d_bayesian_seasonal_adj.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_bayesian_seasonal_adj('
    evalstring += 'c_int(nobs)'
    evalstring += ','
    w = toNumpyArray(w, 'w', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'w.ctypes.data_as(c_void_p)'
    nobs = shape[0]
    if not (trendOrder is None):
        evalstring += ','
        evalstring += repr(IMSLS_TREND_ORDER)
        evalstring += ','
        evalstring += 'c_int(trendOrder)'
    if not (seasonalOrder is None):
        evalstring += ','
        evalstring += repr(IMSLS_SEASONAL_ORDER)
        evalstring += ','
        evalstring += 'c_int(seasonalOrder)'
    if not (numPredict is None):
        evalstring += ','
        evalstring += repr(IMSLS_NUM_PREDICT)
        evalstring += ','
        evalstring += 'c_int(numPredict)'
#        nPredict = numPredict
#    else:
#        nPredict = 0
    if not (period is None):
        evalstring += ','
        evalstring += repr(IMSLS_PERIOD)
        evalstring += ','
        evalstring += 'c_int(period)'
    if not (span is None):
        evalstring += ','
        evalstring += repr(IMSLS_SPAN)
        evalstring += ','
        evalstring += 'c_int(span)'
    if not (rigidity is None):
        evalstring += ','
        evalstring += repr(IMSLS_RIGIDITY)
        evalstring += ','
        evalstring += 'c_double(rigidity)'
    if not (model is None):
        evalstring += ','
        evalstring += repr(IMSLS_MODEL)
        evalstring += ','
        evalstring += 'c_int(model)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (nonseasonalTrend is None):
        evalstring += ','
        evalstring += repr(IMSLS_NONSEASONAL_TREND)
        checkForList(nonseasonalTrend, 'nonseasonalTrend')
        evalstring += ','
        nonseasonalTrend_trend_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(nonseasonalTrend_trend_tmp)'
    if not (seasonal is None):
        evalstring += ','
        evalstring += repr(IMSLS_SEASONAL)
        checkForList(seasonal, 'seasonal')
        evalstring += ','
        seasonal_seasonal_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(seasonal_seasonal_tmp)'
    if not (irregularComponents is None):
        evalstring += ','
        evalstring += repr(IMSLS_IRREGULAR_COMPONENTS)
        checkForList(irregularComponents, 'irregularComponents')
        evalstring += ','
        irregularComponents_irrComp_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(irregularComponents_irrComp_tmp)'
    if not (seriesSmoothed is None):
        evalstring += ','
        evalstring += repr(IMSLS_SERIES_SMOOTHED)
        checkForList(seriesSmoothed, 'seriesSmoothed')
        evalstring += ','
        seriesSmoothed_smoothed_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(seriesSmoothed_smoothed_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nonseasonalTrend is None):
        processRet(nonseasonalTrend_trend_tmp, shape=(
            nobs + numPredict), pyvar=nonseasonalTrend)
    if not (seasonal is None):
        processRet(seasonal_seasonal_tmp, shape=(
            nobs + numPredict), pyvar=seasonal)
    if not (irregularComponents is None):
        processRet(irregularComponents_irrComp_tmp,
                   shape=(nobs), pyvar=irregularComponents)
    if not (seriesSmoothed is None):
        processRet(seriesSmoothed_smoothed_tmp, shape=(
            nobs + numPredict), pyvar=seriesSmoothed)
    return result
