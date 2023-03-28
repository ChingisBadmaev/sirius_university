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
from pyimsl.util.VersionFacade import VersionFacade
from numpy import array, empty
from ctypes import *

IMSLS_N_MISSING = 13440
IMSLS_XLO = 50490
IMSLS_XHI = 50492
imslstat = loadimsl(STAT)


def empiricalQuantiles(x, qprop, nMissing=None, xlo=None, xhi=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_empirical_quantiles.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_empirical_quantiles('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(nQprop)'
    evalstring += ','
    qprop = toNumpyArray(qprop, 'qprop', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'qprop.ctypes.data_as(c_void_p)'
    nQprop = shape[0]
    if not (nMissing is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING)
        checkForList(nMissing, 'nMissing')
        evalstring += ','
        nMissing_nMiss_tmp = c_int()
        evalstring += 'byref(nMissing_nMiss_tmp)'
    if not (xlo is None):
        evalstring += ','
        evalstring += repr(IMSLS_XLO)
        checkForList(xlo, 'xlo')
        evalstring += ','
        xlo_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xlo_tmp)'
    if not (xhi is None):
        evalstring += ','
        evalstring += repr(IMSLS_XHI)
        checkForList(xhi, 'xhi')
        evalstring += ','
        xhi_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xhi_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nMissing is None):
        processRet(nMissing_nMiss_tmp, shape=(1), pyvar=nMissing)
    if not (xlo is None):
        processRet(xlo_tmp, shape=(nQprop), pyvar=xlo)
    if not (xhi is None):
        processRet(xhi_tmp, shape=(nQprop), pyvar=xhi)
    return processRet(result, shape=(nQprop), result=True)
