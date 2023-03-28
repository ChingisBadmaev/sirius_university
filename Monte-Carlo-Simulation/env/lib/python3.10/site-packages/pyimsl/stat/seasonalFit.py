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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_D_INITIAL = 50170
IMSLS_SET_FIRST_TO_NAN = 14500
IMSLS_EXCLUDE_FIRST = 11540
IMSLS_CENTER = 25390
IMSLS_LOST = 12840
IMSLS_BEST_PERIODS = 50120
IMSLS_BEST_ORDERS = 50140
IMSLS_AR_ORDER = 50160
IMSLS_AIC = 30042
imslstat = loadimsl(STAT)


def seasonalFit(z, maxlag, sInitial, dInitial=None, setFirstToNan=None, excludeFirst=None, center=None, lost=None, bestPeriods=None, bestOrders=None, arOrder=None, aic=None):
    """ Estimates the optimum seasonality parameters for a time series using an autoregressive model to represent the time series.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_seasonal_fit.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_seasonal_fit('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    z = toNumpyArray(z, 'z', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'z.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    evalstring += 'c_int(maxlag)'
    evalstring += ','
    evalstring += 'c_int(nDifferences)'
    evalstring += ','
    evalstring += 'c_int(nSInitial)'
    evalstring += ','
    sInitial = toNumpyArray(sInitial, 'sInitial',
                            shape=shape, dtype='int', expectedShape=(0, 0))
    evalstring += 'sInitial.ctypes.data_as(c_void_p)'
    nSInitial = shape[0]
    nDifferences = shape[1]
    if not (dInitial is None):
        evalstring += ','
        evalstring += repr(IMSLS_D_INITIAL)
        evalstring += ','
        evalstring += 'c_int(initial_nDInitial_tmp)'
        evalstring += ','
        initial_dInitial_tmp = toNumpyArray(
            dInitial, 'dInitial', shape=shape, dtype='int', expectedShape=(0, nDifferences))
        evalstring += 'initial_dInitial_tmp.ctypes.data_as(c_void_p)'
        initial_nDInitial_tmp = shape[0]
    checkForBoolean(setFirstToNan, 'setFirstToNan')
    if (setFirstToNan):
        evalstring += ','
        evalstring += repr(IMSLS_SET_FIRST_TO_NAN)
    checkForBoolean(excludeFirst, 'excludeFirst')
    if (excludeFirst):
        evalstring += ','
        evalstring += repr(IMSLS_EXCLUDE_FIRST)
    if not (center is None):
        evalstring += ','
        evalstring += repr(IMSLS_CENTER)
        evalstring += ','
        evalstring += 'c_int(center)'
    if not (lost is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOST)
        checkForList(lost, 'lost')
        evalstring += ','
        lost_lost_tmp = c_int()
        evalstring += 'byref(lost_lost_tmp)'
    if not (bestPeriods is None):
        evalstring += ','
        evalstring += repr(IMSLS_BEST_PERIODS)
        checkForList(bestPeriods, 'bestPeriods')
        evalstring += ','
        bestPeriods_bestPeriods_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(bestPeriods_bestPeriods_tmp)'
    if not (bestOrders is None):
        evalstring += ','
        evalstring += repr(IMSLS_BEST_ORDERS)
        checkForList(bestOrders, 'bestOrders')
        evalstring += ','
        bestOrders_bestOrders_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(bestOrders_bestOrders_tmp)'
    if not (arOrder is None):
        evalstring += ','
        evalstring += repr(IMSLS_AR_ORDER)
        checkForList(arOrder, 'arOrder')
        evalstring += ','
        arOrder_arOrder_tmp = c_int()
        evalstring += 'byref(arOrder_arOrder_tmp)'
    if not (aic is None):
        evalstring += ','
        evalstring += repr(IMSLS_AIC)
        checkForList(aic, 'aic')
        evalstring += ','
        aic_aic_tmp = c_double()
        evalstring += 'byref(aic_aic_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (lost is None):
        processRet(lost_lost_tmp, shape=1, pyvar=lost)
    if not (bestPeriods is None):
        processRet(bestPeriods_bestPeriods_tmp, shape=(
            nDifferences), pyvar=bestPeriods)
    if not (bestOrders is None):
        processRet(bestOrders_bestOrders_tmp, shape=(
            nDifferences), pyvar=bestOrders)
    if not (arOrder is None):
        processRet(arOrder_arOrder_tmp, shape=1, pyvar=arOrder)
    if not (aic is None):
        processRet(aic_aic_tmp, shape=1, pyvar=aic)
    return processRet(result, shape=(nObs), result=True)
