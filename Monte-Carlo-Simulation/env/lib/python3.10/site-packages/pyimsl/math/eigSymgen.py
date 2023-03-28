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
from pyimsl.util.imslUtils import MATH, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_VECTORS = 10094
IMSL_RANGE = 10097
IMSL_A_COL_DIM = 10003
IMSL_B_COL_DIM = 10186
IMSL_EVECU_COL_DIM = 10096
imslmath = loadimsl(MATH)


def eigSymgen(a, b, vectors=None, range=None, aColDim=None, bColDim=None, evecuColDim=None):
    """ Computes the generalized eigenexpansion of a system Ax = .Bx. The matrices A and B are real and symmetric, and B is positive definite.
    """
    imslmath.imsl_d_eig_symgen.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_eig_symgen('
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(n, n))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    if not (vectors is None):
        evalstring += ','
        evalstring += repr(IMSL_VECTORS)
        checkForList(vectors, 'vectors')
        evalstring += ','
        vectors_evec_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(vectors_evec_tmp)'
    if not (range is None):
        evalstring += ','
        evalstring += repr(IMSL_RANGE)
        checkForDict(range, 'range', ['elow', 'ehigh'])
        evalstring += ','
        range_elow_tmp = range['elow']
        evalstring += 'c_double(range_elow_tmp)'
        evalstring += ','
        range_ehigh_tmp = range['ehigh']
        evalstring += 'c_double(range_ehigh_tmp)'
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
    if not (vectors is None):
        processRet(vectors_evec_tmp, shape=(n, n), pyvar=vectors)
    return processRet(result, shape=(n), result=True)
