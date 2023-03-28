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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_survival

IMSLS_XBETA = 20685
imslstat = loadimsl(STAT)


def survivalEstimates(survivalInfo, nEstimates, xpt, time, npt, delta, xbeta=None):
    """ Estimates survival probabilities and hazard rates for the various parametric models.
    """
    imslstat.imsls_d_survival_estimates.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_survival_estimates('
    evalstring += 'survivalInfo'
    evalstring += ','
    evalstring += 'c_int(nEstimates)'
    evalstring += ','
    xpt = toNumpyArray(xpt, 'xpt', shape=shape,
                       dtype='double', expectedShape=(0, 0))
    evalstring += 'xpt.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_double(time)'
    evalstring += ','
    evalstring += 'c_int(npt)'
    evalstring += ','
    evalstring += 'c_double(delta)'
    if not (xbeta is None):
        evalstring += ','
        evalstring += repr(IMSLS_XBETA)
        checkForList(xbeta, 'xbeta')
        evalstring += ','
        xbeta_xbeta_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(xbeta_xbeta_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (xbeta is None):
        processRet(xbeta_xbeta_tmp, shape=(nObservations), pyvar=xbeta)
    return processRet(result, shape=(npt, (2 * nEstimates) + 1), result=True)
