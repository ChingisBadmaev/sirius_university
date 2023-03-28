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
from pyimsl.util.imslUtils import STAT, checkForBoolean, fatalErrorCheck, loadimsl, processRet
from numpy import mean, shape
from ctypes import POINTER, c_double, c_int
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_MEAN = 20410
IMSLS_VARIANCE = 20420
IMSLS_ACCEPT_REJECT_METHOD = 20430
IMSLS_ZIGGURAT_METHOD = 50629
imslstat = loadimsl(STAT)


def randomNormal(nRandom, mean=None, variance=None, acceptRejectMethod=None, zigguratMethod=None):
    """ Generates pseudorandom numbers from a normal distribution.
    """
    imslstat.imsls_d_random_normal.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_normal('
    evalstring += 'c_int(nRandom)'
    if not (mean is None):
        evalstring += ','
        evalstring += repr(IMSLS_MEAN)
        evalstring += ','
        evalstring += 'c_double(mean)'
    if not (variance is None):
        evalstring += ','
        evalstring += repr(IMSLS_VARIANCE)
        evalstring += ','
        evalstring += 'c_double(variance)'
    checkForBoolean(acceptRejectMethod, 'acceptRejectMethod')
    if (acceptRejectMethod):
        evalstring += ','
        evalstring += repr(IMSLS_ACCEPT_REJECT_METHOD)
    # zigguratMethod is new with CNL 7.
    checkForBoolean(zigguratMethod, 'zigguratMethod')
    if (zigguratMethod):
        VersionFacade.checkVersion(7)
        evalstring += ','
        evalstring += repr(IMSLS_ZIGGURAT_METHOD)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nRandom), result=True)
