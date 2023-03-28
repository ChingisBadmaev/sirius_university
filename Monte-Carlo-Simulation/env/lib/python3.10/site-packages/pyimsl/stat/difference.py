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
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_ORDERS = 13620
IMSLS_LOST = 12840
IMSLS_EXCLUDE_FIRST = 11540
IMSLS_SET_FIRST_TO_NAN = 14500
imslstat = loadimsl(STAT)


def difference(z, periods, orders=None, lost=None, excludeFirst=None, setFirstToNan=None):
    """ Differences a seasonal or nonseasonal time series.
    """
    imslstat.imsls_d_difference.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_difference('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    z = toNumpyArray(z, 'z', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'z.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(nDifferences)'
    evalstring += ','
    periods = toNumpyArray(periods, 'periods', shape=shape,
                           dtype='int', expectedShape=(0))
    evalstring += 'periods.ctypes.data_as(c_void_p)'
    nDifferences = shape[0]
    if not (orders is None):
        evalstring += ','
        evalstring += repr(IMSLS_ORDERS)
        evalstring += ','
        orders = toNumpyArray(orders, 'orders', shape=shape,
                              dtype='int', expectedShape=(nDifferences))
        evalstring += 'orders.ctypes.data_as(c_void_p)'
    if not (lost is None):
        evalstring += ','
        evalstring += repr(IMSLS_LOST)
        checkForList(lost, 'lost')
        evalstring += ','
        lost_lost_tmp = c_int()
        evalstring += 'byref(lost_lost_tmp)'
    checkForBoolean(excludeFirst, 'excludeFirst')
    if (excludeFirst):
        evalstring += ','
        evalstring += repr(IMSLS_EXCLUDE_FIRST)
    checkForBoolean(setFirstToNan, 'setFirstToNan')
    if (setFirstToNan):
        evalstring += ','
        evalstring += repr(IMSLS_SET_FIRST_TO_NAN)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (lost is None):
        processRet(lost_lost_tmp, shape=1, pyvar=lost)
    return processRet(result, shape=(nObservations), result=True)
