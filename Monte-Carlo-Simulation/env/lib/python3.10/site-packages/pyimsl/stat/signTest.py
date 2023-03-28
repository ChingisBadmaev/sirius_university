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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, processRet
from numpy import double, dtype, shape
from ctypes import byref, c_double, c_int, c_void_p

IMSLS_PERCENTAGE = 13720
IMSLS_PERCENTILE = 13730
IMSLS_N_POSITIVE_DEVIATIONS = 13460
IMSLS_N_ZERO_DEVIATIONS = 15830
imslstat = loadimsl(STAT)


def signTest(x, percentage=None, percentile=None, nPositiveDeviations=None, nZeroDeviations=None):
    """ Performs a sign test.
    """
    imslstat.imsls_d_sign_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_sign_test('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    if not (percentage is None):
        evalstring += ','
        evalstring += repr(IMSLS_PERCENTAGE)
        evalstring += ','
        evalstring += 'c_double(percentage)'
    if not (percentile is None):
        evalstring += ','
        evalstring += repr(IMSLS_PERCENTILE)
        evalstring += ','
        evalstring += 'c_double(percentile)'
    if not (nPositiveDeviations is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_POSITIVE_DEVIATIONS)
        checkForList(nPositiveDeviations, 'nPositiveDeviations')
        evalstring += ','
        nPositiveDeviations_nPositiveDeviations_tmp = c_int()
        evalstring += 'byref(nPositiveDeviations_nPositiveDeviations_tmp)'
    if not (nZeroDeviations is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ZERO_DEVIATIONS)
        checkForList(nZeroDeviations, 'nZeroDeviations')
        evalstring += ','
        nZeroDeviations_nZeroDeviations_tmp = c_int()
        evalstring += 'byref(nZeroDeviations_nZeroDeviations_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nPositiveDeviations is None):
        processRet(nPositiveDeviations_nPositiveDeviations_tmp,
                   shape=1, pyvar=nPositiveDeviations)
    if not (nZeroDeviations is None):
        processRet(nZeroDeviations_nZeroDeviations_tmp,
                   shape=1, pyvar=nZeroDeviations)
    return result
