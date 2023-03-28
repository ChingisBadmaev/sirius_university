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

IMSLS_DIFFERENCES = 30018
IMSLS_N_MISSING_X = 30020
IMSLS_N_MISSING_Y = 30021
imslstat = loadimsl(STAT)


def kolmogorovTwo(x, y, differences=None, nMissingX=None, nMissingY=None):
    """ Performs a Kolmogorov-Smirnov two-sample test.
    """
    imslstat.imsls_d_kolmogorov_two.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_kolmogorov_two('
    evalstring += 'c_int(nObservationsX)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservationsX = shape[0]
    evalstring += ','
    evalstring += 'c_int(nObservationsY)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    nObservationsY = shape[0]
    if not (differences is None):
        evalstring += ','
        evalstring += repr(IMSLS_DIFFERENCES)
        checkForList(differences, 'differences')
        evalstring += ','
        differences_differences_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(differences_differences_tmp)'
    if not (nMissingX is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING_X)
        checkForList(nMissingX, 'nMissingX')
        evalstring += ','
        nMissingX_xmissing_tmp = c_int()
        evalstring += 'byref(nMissingX_xmissing_tmp)'
    if not (nMissingY is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_MISSING_Y)
        checkForList(nMissingY, 'nMissingY')
        evalstring += ','
        nMissingY_ymissing_tmp = c_int()
        evalstring += 'byref(nMissingY_ymissing_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (differences is None):
        processRet(differences_differences_tmp, shape=(3), pyvar=differences)
    if not (nMissingX is None):
        processRet(nMissingX_xmissing_tmp, shape=1, pyvar=nMissingX)
    if not (nMissingY is None):
        processRet(nMissingY_ymissing_tmp, shape=1, pyvar=nMissingY)
    return processRet(result, shape=(3), result=True)
