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
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_SHAPIRO_WILK_W = 14550
imslstat = loadimsl(STAT)


def shapiroWilkNormalityTest(x, shapiroWilkW=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_shapiro_wilk_normality_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_shapiro_wilk_normality_test('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (shapiroWilkW is None):
        evalstring += ','
        evalstring += repr(IMSLS_SHAPIRO_WILK_W)
        checkForList(shapiroWilkW, 'shapiroWilkW')
        evalstring += ','
        shapiroWilkW_shapiroWilkW_tmp = c_double()
        evalstring += 'byref(shapiroWilkW_shapiroWilkW_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (shapiroWilkW is None):
        processRet(shapiroWilkW_shapiroWilkW_tmp,
                   shape=(1), pyvar=shapiroWilkW)
    return result
