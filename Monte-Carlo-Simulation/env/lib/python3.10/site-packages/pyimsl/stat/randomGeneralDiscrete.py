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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_GET_INDEX_VECTORS = 40001
IMSLS_SET_INDEX_VECTORS = 40003
IMSLS_TABLE = 14950
imslstat = loadimsl(STAT)


def randomGeneralDiscrete(nRandom, imin, nmass, probs, getIndexVectors=None, setIndexVectors=None, table=None):
    """ Generates pseudorandom numbers from a general discrete distribution using an alias method or optionally a table lookup method.
    """
    imslstat.imsls_d_random_general_discrete.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_d_random_general_discrete('
    evalstring += 'c_int(nRandom)'
    evalstring += ','
    evalstring += 'c_int(imin)'
    evalstring += ','
    evalstring += 'c_int(nmass)'
    evalstring += ','
    probs = toNumpyArray(probs, 'probs', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'probs.ctypes.data_as(c_void_p)'
    # nmass=shape[0]
    if not (getIndexVectors is None):
        evalstring += ','
        evalstring += repr(IMSLS_GET_INDEX_VECTORS)
        checkForDict(getIndexVectors, 'getIndexVectors', [])
        evalstring += ','
        getIndexVectors_iwk_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(getIndexVectors_iwk_tmp)'
        evalstring += ','
        getIndexVectors_wk_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(getIndexVectors_wk_tmp)'
    if not (setIndexVectors is None):
        evalstring += ','
        evalstring += repr(IMSLS_SET_INDEX_VECTORS)
        checkForDict(setIndexVectors, 'setIndexVectors', ['iwk', 'wk'])
        evalstring += ','
        setIndexVectors_iwk_tmp = setIndexVectors['iwk']
        setIndexVectors_iwk_tmp = toNumpyArray(
            setIndexVectors_iwk_tmp, 'iwk', shape=shape, dtype='int', expectedShape=(nmass))
        evalstring += 'setIndexVectors_iwk_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        setIndexVectors_wk_tmp = setIndexVectors['wk']
        setIndexVectors_wk_tmp = toNumpyArray(
            setIndexVectors_wk_tmp, 'wk', shape=shape, dtype='double', expectedShape=(nmass))
        evalstring += 'setIndexVectors_wk_tmp.ctypes.data_as(c_void_p)'
    checkForBoolean(table, 'table')
    if (table):
        evalstring += ','
        evalstring += repr(IMSLS_TABLE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (getIndexVectors is None):
        processRet(getIndexVectors_iwk_tmp, shape=(nmass),
                   key='iwk', pyvar=getIndexVectors, createArray=True)
        processRet(getIndexVectors_wk_tmp, shape=(nmass), key='wk',
                   pyvar=getIndexVectors, createArray=True)
    return processRet(result, shape=(nRandom), result=True)
