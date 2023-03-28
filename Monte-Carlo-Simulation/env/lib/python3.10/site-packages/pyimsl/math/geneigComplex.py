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
from pyimsl.util.imslUtils import MATH, checkForList, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import array, complex, double, dtype, shape, zeros
from ctypes import POINTER, byref, c_int
from .mathStructs import d_complex

IMSL_VECTORS = 10094
IMSL_A_COL_DIM = 10003
IMSL_B_COL_DIM = 10186
IMSL_EVECU_COL_DIM = 10096
imslmath = loadimsl(MATH)


def geneigComplex(a, b, alpha, beta, vectors=None, aColDim=None, bColDim=None, evecuColDim=None):
    """ Computes the generalized eigenexpansion of a system Ax = .Bx, with A and B complex.
    """
    imslmath.imsl_z_geneig.restype = None
    shape = []
    evalstring = 'imslmath.imsl_z_geneig('
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='d_complex',
                     expectedShape=(0, 0))
    evalstring += 'a'
    n = shape[0]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='d_complex',
                     expectedShape=(n, n))
    evalstring += 'b'
    evalstring += ','
#
#   Alpha and beta must be preallocated before the call
#   Note that toNumpyArray doesn't create a numpy array for arrays
#   of complex, so we don't need to do ...ctypes.data_as... for alpha or beta
#
    alpha_tmp_tmp = zeros((n), dtype='double')
    beta_tmp_tmp = zeros((n), dtype='double')
    alpha_tmp = toNumpyArray(alpha_tmp_tmp, 'alpha',
                             shape=shape, dtype='d_complex')
    evalstring += 'alpha_tmp'
    evalstring += ','
    beta_tmp = toNumpyArray(beta_tmp_tmp, 'beta',
                            shape=shape, dtype='d_complex')
    evalstring += 'beta_tmp'
    if not (vectors is None):
        evalstring += ','
        evalstring += repr(IMSL_VECTORS)
        checkForList(vectors, 'vectors')
        evalstring += ','
        vectors_evec_tmp = POINTER(d_complex)(d_complex())
        evalstring += 'byref(vectors_evec_tmp)'
    if not (aColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_A_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(aColDim)'
    if not (bColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_B_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(bColDim)'
    if not (evecuColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_EVECU_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(evecuColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if isinstance(alpha, list):
        alpha[:] = []
    processRet(alpha_tmp, shape=(n), pyvar=alpha, freemem=False)
    if isinstance(beta, list):
        beta[:] = []
    processRet(beta_tmp, shape=(n), pyvar=beta, freemem=False)
    if not (vectors is None):
        processRet(vectors_evec_tmp, shape=(n, n), pyvar=vectors)
    return
