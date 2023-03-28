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
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_LAGMIN = 30008
imslstat = loadimsl(STAT)


def lackOfFit(nObservations, cf, lagmax, npfree, lagmin=None):
    """ Performs lack-of-fit test for a univariate time series or transfer function given the appropriate correlation function.
    """
    imslstat.imsls_d_lack_of_fit.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_lack_of_fit('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    cf = toNumpyArray(cf, 'cf', shape=shape, dtype='double',
                      expectedShape=(lagmax + 1))
    evalstring += 'cf.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(lagmax)'
    evalstring += ','
    evalstring += 'c_int(npfree)'
    if not (lagmin is None):
        evalstring += ','
        evalstring += repr(IMSLS_LAGMIN)
        evalstring += ','
        evalstring += 'c_int(lagmin)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(2), result=True)
