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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, byref, c_double, c_int
from .statStructs import Imsls_d_arma

IMSLS_CONFIDENCE = 10860
IMSLS_BACKWARD_ORIGIN = 10210
IMSLS_ONE_STEP_FORECAST = 10211
imslstat = loadimsl(STAT)


def armaForecast(armaInfo, nPredict, confidence=None, backwardOrigin=None, oneStepForecast=None):
    """ Computes forecasts and their associated probability limits for an ARMA model.
    """
    imslstat.imsls_d_arma_forecast.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_arma_forecast('
    evalstring += 'armaInfo'
    evalstring += ','
    evalstring += 'c_int(nPredict)'
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (backwardOrigin is None):
        evalstring += ','
        evalstring += repr(IMSLS_BACKWARD_ORIGIN)
        evalstring += ','
        evalstring += 'c_int(backwardOrigin)'
    else:
        backwardOrigin = 0
    if not (oneStepForecast is None):
        evalstring += ','
        evalstring += repr(IMSLS_ONE_STEP_FORECAST)
        checkForList(oneStepForecast, 'oneStepForecast')
        evalstring += ','
        oneStepForecast_forecast_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(oneStepForecast_forecast_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (oneStepForecast is None):
        processRet(oneStepForecast_forecast_tmp, shape=(
            backwardOrigin + nPredict), pyvar=oneStepForecast)
    return processRet(result, shape=(nPredict, (backwardOrigin + 3)), result=True)
