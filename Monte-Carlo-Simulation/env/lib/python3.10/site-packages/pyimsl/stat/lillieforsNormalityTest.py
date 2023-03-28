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

IMSLS_MAX_DIFFERENCE = 12781
imslstat = loadimsl(STAT)


def lillieforsNormalityTest(x, maxDifference=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_lilliefors_normality_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_lilliefors_normality_test('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (maxDifference is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_DIFFERENCE)
        checkForList(maxDifference, 'maxDifference')
        evalstring += ','
        maxDifference_maxDifference_tmp = c_double()
        evalstring += 'byref(maxDifference_maxDifference_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (maxDifference is None):
        processRet(maxDifference_maxDifference_tmp,
                   shape=(1), pyvar=maxDifference)
    return result
