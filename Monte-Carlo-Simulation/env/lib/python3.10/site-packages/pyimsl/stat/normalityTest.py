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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, checkForDict, processRet
from numpy import double, dtype, shape, size
from ctypes import byref, c_double, c_int, c_void_p

IMSLS_SHAPIRO_WILK_W = 14550
IMSLS_LILLIEFORS = 12780
IMSLS_CHI_SQUARED = 10450
imslstat = loadimsl(STAT)


def normalityTest(x, shapiroWilkW=None, lilliefors=None, chiSquared=None):
    """ Performs a test for normality.
    """
    imslstat.imsls_d_normality_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_normality_test('
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
    if not (lilliefors is None):
        evalstring += ','
        evalstring += repr(IMSLS_LILLIEFORS)
        checkForList(lilliefors, 'lilliefors')
        evalstring += ','
        lilliefors_maxDifference_tmp = c_double()
        evalstring += 'byref(lilliefors_maxDifference_tmp)'
    if not (chiSquared is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED)
        checkForDict(chiSquared, 'chiSquared', ['nCategories'])
        evalstring += ','
        chiSquared_nCategories_tmp = chiSquared['nCategories']
        evalstring += 'c_int(chiSquared_nCategories_tmp)'
        evalstring += ','
        chiSquared_df_tmp = c_double()
        evalstring += 'byref(chiSquared_df_tmp)'
        evalstring += ','
        chiSquared_chiSquared_tmp = c_double()
        evalstring += 'byref(chiSquared_chiSquared_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (shapiroWilkW is None):
        processRet(shapiroWilkW_shapiroWilkW_tmp,
                   shape=(1), pyvar=shapiroWilkW)
    if not (lilliefors is None):
        processRet(lilliefors_maxDifference_tmp, shape=(1), pyvar=lilliefors)
    if not (chiSquared is None):
        processRet(chiSquared_df_tmp, shape=(1), key='df', pyvar=chiSquared)
        processRet(chiSquared_chiSquared_tmp, shape=(
            1), key='chiSquared', pyvar=chiSquared)
    return result
