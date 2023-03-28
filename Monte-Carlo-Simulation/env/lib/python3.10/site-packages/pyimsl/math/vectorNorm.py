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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, processRet
from numpy import double, dtype, shape
from ctypes import byref, c_double, c_int, c_void_p

IMSL_ONE_NORM = 10323
IMSL_INF_NORM = 10324
IMSL_SECOND_VECTOR = 10325
imslmath = loadimsl(MATH)


def vectorNorm(x, oneNorm=None, infNorm=None, secondVector=None):
    """ Computes various norms of a vector or the difference of two vectors.
    """
    imslmath.imsl_d_vector_norm.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_vector_norm('
    evalstring += 'c_int(n)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    n = shape[0]
    checkForBoolean(oneNorm, 'oneNorm')
    if (oneNorm):
        evalstring += ','
        evalstring += repr(IMSL_ONE_NORM)
    if not (secondVector is None):
        evalstring += ','
        evalstring += repr(IMSL_SECOND_VECTOR)
        evalstring += ','
        secondVector = toNumpyArray(
            secondVector, 'secondVector', shape=shape, dtype='double', expectedShape=(n))
        evalstring += 'secondVector.ctypes.data_as(c_void_p)'
    if not (infNorm is None):
        evalstring += ','
        evalstring += repr(IMSL_INF_NORM)
        checkForList(infNorm, 'infNorm')
        evalstring += ','
        infNorm_index_tmp = c_int()
        evalstring += 'byref(infNorm_index_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (infNorm is None):
        processRet(infNorm_index_tmp, shape=1, pyvar=infNorm)
    return result
