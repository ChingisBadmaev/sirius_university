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
from numpy import dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int
from .mathStructs import d_complex
from .mathStructs import d_complex

IMSL_VECTORS = 10094
IMSL_RANGE = 10097
IMSL_A_COL_DIM = 10003
IMSL_EVECU_COL_DIM = 10096
IMSL_RETURN_NUMBER = 10259
imslmath = loadimsl(MATH)


def eigHermComplex(a, vectors=None, range=None, aColDim=None, evecuColDim=None, returnNumber=None):
    """ Computes the eigenexpansion of a complex Hermitian matrix A.
    """
    imslmath.imsl_z_eig_herm.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_z_eig_herm('
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='d_complex',
                     expectedShape=(0, 0))
    evalstring += 'a'
    n = shape[0]
    if not (vectors is None):
        evalstring += ','
        evalstring += repr(IMSL_VECTORS)
        checkForList(vectors, 'vectors')
        evalstring += ','
        vectors_evec_tmp = POINTER(d_complex)(d_complex())
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
    if not (evecuColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_EVECU_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(evecuColDim)'
    if not (returnNumber is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_NUMBER)
        checkForList(returnNumber, 'returnNumber')
        evalstring += ','
        returnNumber_nEval_tmp = c_int()
        evalstring += 'byref(returnNumber_nEval_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (vectors is None):
        processRet(vectors_evec_tmp, shape=(n, n), pyvar=vectors)
    if not (returnNumber is None):
        processRet(returnNumber_nEval_tmp, shape=1, pyvar=returnNumber)
    return processRet(result, shape=(n), result=True)
