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
from pyimsl.util.imslUtils import MATH, checkForBoolean, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import dtype, shape
from ctypes import POINTER, byref, c_int
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex

IMSL_A_TRANSPOSE = 11145
IMSL_B_TRANSPOSE = 11146
IMSL_A_CONJUGATE_TRANSPOSE = 11147
IMSL_B_CONJUGATE_TRANSPOSE = 11148
IMSL_SYMMETRIC = 11150
imslmath = loadimsl(MATH)


def matAddBandComplex(nlca, nuca, alpha, a, nlcb, nucb, beta, b, nlcc, nucc, aTranspose=None, bTranspose=None, aConjugateTranspose=None, bConjugateTranspose=None, symmetric=None):
    """ Adds two band matrices, both in band storage mode,
    """
    imslmath.imsl_z_mat_add_band.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_mat_add_band('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nlca)'
    evalstring += ','
    evalstring += 'c_int(nuca)'
    evalstring += ','
    alpha = toNumpyArray(alpha, 'alpha', shape=shape,
                         dtype='d_complex', expectedShape=(1))
    evalstring += 'alpha'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='d_complex',
                     expectedShape=(nlca + nuca + 1, 0))
    evalstring += 'a'
    n = shape[1]
    evalstring += ','
    evalstring += 'c_int(nlcb)'
    evalstring += ','
    evalstring += 'c_int(nucb)'
    evalstring += ','
    beta = toNumpyArray(beta, 'beta', shape=shape,
                        dtype='d_complex', expectedShape=(1))
    evalstring += 'beta'
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='d_complex',
                     expectedShape=(nlcb + nucb + 1, n))
    evalstring += 'b'
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
    checkForBoolean(aConjugateTranspose, 'aConjugateTranspose')
    if (aConjugateTranspose):
        evalstring += ','
        evalstring += repr(IMSL_A_CONJUGATE_TRANSPOSE)
    checkForBoolean(bConjugateTranspose, 'bConjugateTranspose')
    if (bConjugateTranspose):
        evalstring += ','
        evalstring += repr(IMSL_B_CONJUGATE_TRANSPOSE)
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
