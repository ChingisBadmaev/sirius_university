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
from pyimsl.util.imslUtils import MATH, checkForBoolean, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import c_double, c_int, c_void_p

IMSL_ONE_NORM = 10323
IMSL_INF_NORM = 10324
imslmath = loadimsl(MATH)


def matrixNorm(a, oneNorm=None, infNorm=None):
    """ Computes various norms of a rectangular matrix.
    """
    imslmath.imsl_d_matrix_norm.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_matrix_norm('
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    m = shape[0]
    n = shape[1]
    checkForBoolean(oneNorm, 'oneNorm')
    if (oneNorm):
        evalstring += ','
        evalstring += repr(IMSL_ONE_NORM)
    checkForBoolean(infNorm, 'infNorm')
    if (infNorm):
        evalstring += ','
        evalstring += repr(IMSL_INF_NORM)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
