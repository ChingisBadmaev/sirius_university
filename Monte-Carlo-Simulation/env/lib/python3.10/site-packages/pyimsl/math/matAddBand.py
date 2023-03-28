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
from pyimsl.util.imslUtils import MATH, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_A_TRANSPOSE = 11145
IMSL_B_TRANSPOSE = 11146
IMSL_SYMMETRIC = 11150
imslmath = loadimsl(MATH)


def matAddBand(nlca, nuca, alpha, a, nlcb, nucb, beta, b, nlcc, nucc, aTranspose=None, bTranspose=None, symmetric=None):
    """ Adds two band matrices, both in band storage mode.
    """
    imslmath.imsl_d_mat_add_band.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_mat_add_band('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nlca)'
    evalstring += ','
    evalstring += 'c_int(nuca)'
    evalstring += ','
    evalstring += 'c_double(alpha)'
    evalstring += ','
    checkForBoolean(symmetric, 'symmetric')
    if (symmetric):
        expShape = (nlca + 1, 0)
    else:
        expShape = (nlca + nuca + 1, 0)
    a = toNumpyArray(a, 'a', shape=shape, dtype='double',
                     expectedShape=expShape)
    evalstring += 'a.ctypes.data_as(c_void_p)'
    n = shape[1]
    evalstring += ','
    evalstring += 'c_int(nlcb)'
    evalstring += ','
    evalstring += 'c_int(nucb)'
    evalstring += ','
    evalstring += 'c_double(beta)'
    evalstring += ','
    checkForBoolean(symmetric, 'symmetric')
    if (symmetric):
        expShape = (nlcb + 1, 0)
    else:
        expShape = (nlcb + nucb + 1, 0)
    b = toNumpyArray(b, 'b', shape=shape, dtype='double',
                     expectedShape=expShape)
    evalstring += 'b.ctypes.data_as(c_void_p)'
    evalstring += ','
    nlcc_tmp = c_int()
    evalstring += 'byref(nlcc_tmp)'
    evalstring += ','
    nucc_tmp = c_int()
    evalstring += 'byref(nucc_tmp)'
    checkForBoolean(aTranspose, 'aTranspose')
    if (aTranspose):
        evalstring += ','
        evalstring += repr(IMSL_A_TRANSPOSE)
    checkForBoolean(bTranspose, 'bTranspose')
    if (bTranspose):
        evalstring += ','
        evalstring += repr(IMSL_B_TRANSPOSE)
    checkForBoolean(symmetric, 'symmetric')
    if (symmetric):
        evalstring += ','
        evalstring += repr(IMSL_SYMMETRIC)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if isinstance(nlcc, list):
        nlcc[:] = []
    processRet(nlcc_tmp, shape=1, pyvar=nlcc)
    if isinstance(nucc, list):
        nucc[:] = []
    processRet(nucc_tmp, shape=1, pyvar=nucc)
    return processRet(result, shape=(nlcc_tmp.value + nucc_tmp.value + 1, n), result=True)
