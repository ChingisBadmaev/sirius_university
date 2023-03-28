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
from pyimsl.util.imslUtils import STAT, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from pyimsl.util.Translator import Translator
from numpy import dtype, int, shape
from ctypes import POINTER, byref, c_int, c_void_p

IMSLS_ENCODE = 40514
IMSLS_DECODE = 40515
imslstat = loadimsl(STAT)


def unsupervisedNominalFilter(nClasses, x, encode=None, decode=None):
    """ Converts nominal data into a series of binary encoded columns for input to a neural network.
    """
    VersionFacade.checkVersion(6)
    checkForBoolean(encode, 'encode')
    checkForBoolean(decode, 'decode')
    if not decode:
        encode = True  # Documented default value if neither specified
    # if ((encode is None) and (decode is None)) or ((not(encode is None)) and (not(decode is None))):
    #    errStr = Translator.getString ("encodeError")
    #    raise ValueError, errStr
    imslstat.imsls_unsupervised_nominal_filter.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_unsupervised_nominal_filter('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    if (encode):
        nClasses_tmp = c_int(0)
    else:
        nClasses_tmp = c_int(nClasses)
    evalstring += 'byref(nClasses_tmp)'
    evalstring += ','
    checkForBoolean(encode, 'encode')
    if (encode):
        x = toNumpyArray(x, 'x', shape=shape, dtype='int', expectedShape=(0))
        nObs = shape[0]
    else:
        x = toNumpyArray(x, 'x', shape=shape, dtype='int',
                         expectedShape=(0, nClasses))
        nObs = shape[0]
    evalstring += 'x.ctypes.data_as(c_void_p)'
    checkForBoolean(encode, 'encode')
    if (encode):
        evalstring += ','
        evalstring += repr(IMSLS_ENCODE)
    checkForBoolean(decode, 'decode')
    if (decode):
        evalstring += ','
        evalstring += repr(IMSLS_DECODE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    checkForBoolean(encode, 'encode')
    if (encode):
        processRet(nClasses_tmp, inout=True, pyvar=nClasses)
        return processRet(result, shape=(nObs, nClasses_tmp.value), result=True)
    checkForBoolean(decode, 'decode')
    if (decode):
        return processRet(result, shape=(nObs), result=True)
