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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from pyimsl.util.Translator import Translator
from numpy import double, dtype, int, shape, zeros
from ctypes import byref, c_int, c_void_p

IMSLS_ENCODE = 40514
IMSLS_DECODE = 40515
IMSLS_NO_TRANSFORM = 40516
IMSLS_SQUARE_ROOT = 40517
IMSLS_ARC_SIN = 40518
IMSLS_N_CLASSES = 40521
imslstat = loadimsl(STAT)


def unsupervisedOrdinalFilter(x, z, encode=None, decode=None, noTransform=None, squareRoot=None, arcSin=None, nClasses=None):
    """ Converts ordinal data into proportions.
    """
    VersionFacade.checkVersion(6)
    checkForBoolean(encode, 'encode')
    checkForBoolean(decode, 'decode')
    if not decode:
        encode = True  # Documented default value if neither specified
    # if ((encode is None) and (decode is None)) or ((not(encode is None)) and (not(decode is None))):
    #    errStr = Translator.getString ("encodeError")
    #    raise ValueError, errStr
    imslstat.imsls_d_unsupervised_ordinal_filter.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_unsupervised_ordinal_filter('
    evalstring += 'c_int(nObs)'
    evalstring += ','
    checkForBoolean(encode, 'encode')
    if (encode):
        x_tmp = toNumpyArray(x, 'x', shape=shape,
                             dtype='int', expectedShape=(0))
        nObs = shape[0]
        z_tmp = zeros((nObs))
    else:
        z_tmp = toNumpyArray(z, 'z', shape=shape,
                             dtype='double', expectedShape=(0))
        nObs = shape[0]
        x_tmp = zeros((nObs), dtype='int32')
    evalstring += 'x_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'z_tmp.ctypes.data_as(c_void_p)'

    checkForBoolean(encode, 'encode')
    if (encode):
        evalstring += ','
        evalstring += repr(IMSLS_ENCODE)
    checkForBoolean(decode, 'decode')
    if (decode):
        evalstring += ','
        evalstring += repr(IMSLS_DECODE)
    checkForBoolean(noTransform, 'noTransform')
    if (noTransform):
        evalstring += ','
        evalstring += repr(IMSLS_NO_TRANSFORM)
    checkForBoolean(squareRoot, 'squareRoot')
    if (squareRoot):
        evalstring += ','
        evalstring += repr(IMSLS_SQUARE_ROOT)
    checkForBoolean(arcSin, 'arcSin')
    if (arcSin):
        evalstring += ','
        evalstring += repr(IMSLS_ARC_SIN)
    if not (nClasses is None):
        checkForList(nClasses, 'nClasses')
        nClasses_tmp = c_int(0)
        evalstring += ','
        evalstring += repr(IMSLS_N_CLASSES)
        evalstring += ','
        evalstring += 'byref(nClasses_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(nClasses_tmp, pyvar=nClasses)
    checkForBoolean(encode, 'encode')
    if (encode):
        processRet(z_tmp, shape=(nObs), pyvar=z)
    else:
        processRet(x_tmp, shape=(nObs), pyvar=x)
    return
