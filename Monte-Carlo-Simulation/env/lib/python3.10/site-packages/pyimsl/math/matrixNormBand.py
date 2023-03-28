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
IMSL_SYMMETRIC = 11150
imslmath = loadimsl(MATH)


def matrixNormBand(n, a, nlc, nuc, oneNorm=None, infNorm=None, symmetric=None):
    """ Computes various norms of a matrix stored in band storage mode.
    """
    imslmath.imsl_d_matrix_norm_band.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_matrix_norm_band('
    evalstring += 'c_int(n)'
    evalstring += ','
    checkForBoolean(symmetric, 'symmetric')
    if (symmetric):
        es = (nlc + 1, n)
    else:
        es = (nlc + nuc + 1, n)
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=es)
    evalstring += 'a.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(nlc)'
    evalstring += ','
    evalstring += 'c_int(nuc)'
    checkForBoolean(oneNorm, 'oneNorm')
    if (oneNorm):
        evalstring += ','
        evalstring += repr(IMSL_ONE_NORM)
    checkForBoolean(infNorm, 'infNorm')
    if (infNorm):
        evalstring += ','
        evalstring += repr(IMSL_INF_NORM)
    checkForBoolean(symmetric, 'symmetric')
    if (symmetric):
        evalstring += ','
        evalstring += repr(IMSL_SYMMETRIC)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
