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
from pyimsl.util.imslUtils import STAT, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_SCALE_LIMITS = 40512
IMSLS_SUPPLY_CENTER_SPREAD = 40510
IMSLS_RETURN_CENTER_SPREAD = 40511
imslstat = loadimsl(STAT)


def scaleFilter(x, method, scaleLimits=None, supplyCenterSpread=None, returnCenterSpread=None):
    """ Scales or unscales continuous data prior to its use in neural network training, testing, or forecasting.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_scale_filter.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_scale_filter('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObs = shape[0]
    evalstring += ','
    evalstring += 'c_int(method)'
    if not (scaleLimits is None):
        evalstring += ','
        evalstring += repr(IMSLS_SCALE_LIMITS)
        checkForDict(scaleLimits, 'scaleLimits', [
                     'realMin', 'realMax', 'targetMin', 'targetMax'])
        evalstring += ','
        scaleLimits_realMin_tmp = scaleLimits['realMin']
        evalstring += 'c_double(scaleLimits_realMin_tmp)'
        evalstring += ','
        scaleLimits_realMax_tmp = scaleLimits['realMax']
        evalstring += 'c_double(scaleLimits_realMax_tmp)'
        evalstring += ','
        scaleLimits_targetMin_tmp = scaleLimits['targetMin']
        evalstring += 'c_double(scaleLimits_targetMin_tmp)'
        evalstring += ','
        scaleLimits_targetMax_tmp = scaleLimits['targetMax']
        evalstring += 'c_double(scaleLimits_targetMax_tmp)'
    if not (supplyCenterSpread is None):
        evalstring += ','
        evalstring += repr(IMSLS_SUPPLY_CENTER_SPREAD)
        checkForDict(supplyCenterSpread, 'supplyCenterSpread',
                     ['center', 'spread'])
        evalstring += ','
        supplyCenterSpread_center_tmp = supplyCenterSpread['center']
        evalstring += 'c_double(supplyCenterSpread_center_tmp)'
        evalstring += ','
        supplyCenterSpread_spread_tmp = supplyCenterSpread['spread']
        evalstring += 'c_double(supplyCenterSpread_spread_tmp)'
    if not (returnCenterSpread is None):
        evalstring += ','
        evalstring += repr(IMSLS_RETURN_CENTER_SPREAD)
        checkForDict(returnCenterSpread, 'returnCenterSpread', [])
        evalstring += ','
        returnCenterSpread_center_tmp = c_double()
        evalstring += 'byref(returnCenterSpread_center_tmp)'
        evalstring += ','
        returnCenterSpread_spread_tmp = c_double()
        evalstring += 'byref(returnCenterSpread_spread_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (returnCenterSpread is None):
        processRet(returnCenterSpread_center_tmp, shape=(
            1), key='center', pyvar=returnCenterSpread)
        processRet(returnCenterSpread_spread_tmp, shape=(
            1), key='spread', pyvar=returnCenterSpread)
    return processRet(result, shape=(nObs), result=True)
