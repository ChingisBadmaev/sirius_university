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
from pyimsl.util.imslUtils import Imsl_c_sparse_elem, MATH, checkForBoolean, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import dtype, shape
from ctypes import POINTER, byref, c_int, c_void_p
from .mathStructs import d_complex
from .mathStructs import Imsl_c_sparse_elem

IMSL_A_TRANSPOSE = 11145
IMSL_B_TRANSPOSE = 11146
IMSL_A_CONJUGATE_TRANSPOSE = 11147
IMSL_B_CONJUGATE_TRANSPOSE = 11148
imslmath = loadimsl(MATH)


def matAddCoordinateComplex(n, alpha, a, beta, b, nzC, aTranspose=None, bTranspose=None, aConjugateTranspose=None, bConjugateTranspose=None):
    """ Performs element-wise addition on two complex matrices stored in coordinate format.
    """
    imslmath.imsl_z_mat_add_coordinate.restype = POINTER(Imsl_c_sparse_elem)
    shape = []
    evalstring = 'imslmath.imsl_z_mat_add_coordinate('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nzA)'
    evalstring += ','
    alpha = toNumpyArray(alpha, 'alpha', shape=shape,
                         dtype='d_complex', expectedShape=(1))
    evalstring += 'alpha'
    evalstring += ','
    a_tmp = toNumpyArray(a, 'a', shape=shape,
                         dtype='Imsl_c_sparse_elem', expectedShape=(0, 0))
#    a = toNumpyArray(a, 'a', shape=shape, dtype='struct', expectedShape=(0))
#    evalstring +='a.ctypes.data_as(c_void_p)'
#    nzA=shape[0]
    evalstring += 'a_tmp'
    nzA = len(a)
    evalstring += ','
    evalstring += 'c_int(nzB)'
    evalstring += ','
    beta = toNumpyArray(beta, 'beta', shape=shape,
                        dtype='d_complex', expectedShape=(1))
    evalstring += 'beta'
    evalstring += ','
    b_tmp = toNumpyArray(b, 'b', shape=shape,
                         dtype='Imsl_c_sparse_elem', expectedShape=(0, 0))
#    b = toNumpyArray(b, 'b', shape=shape, dtype='struct', expectedShape=(0))
#    evalstring +='b.ctypes.data_as(c_void_p)'
#    nzB=shape[0]
    evalstring += 'b_tmp'
    nzB = len(b)
    evalstring += ','
    nzC_tmp = c_int()
    evalstring += 'byref(nzC_tmp)'
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
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if isinstance(nzC, list):
        nzC[:] = []
    processRet(nzC_tmp, shape=1, pyvar=nzC)
#    return processRet (result, shape=(nzc), result=True)
    # result is a pointer to Imsl_c_sparse_elem.
    # Imsl_c_sparse struct is made up of row,col, and value
    # but the value is of type d_complex (imsl struct), we need
    # to convert it back to python complex.
    # We can make use of the list to hold both int for rows/cols and complex
    # values.
    res = []
    for i in range(0, nzC[0]):
        temp = result[i].val
        res.append([result[i].row, result[i].col, (complex(temp.re, temp.im))])
    return res
