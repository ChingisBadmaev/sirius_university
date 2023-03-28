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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape, sum
from ctypes import POINTER, c_double, c_int, c_void_p

imslstat = loadimsl(STAT)


def kTrendsTest(ni, y):
    """ Performs a k-sample trends test against ordered alternatives.
    """
    imslstat.imsls_d_k_trends_test.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_k_trends_test('
    evalstring += 'c_int(nGroups)'
    evalstring += ','
    ni = toNumpyArray(ni, 'ni', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'ni.ctypes.data_as(c_void_p)'
    nGroups = shape[0]
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                     expectedShape=sum(ni))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(17), result=True)
