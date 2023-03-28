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
from numpy import dtype, shape
from ctypes import POINTER, byref, c_double, c_int
from .mathStructs import Imsl_d_sparse_elem
from .mathStructs import Imsl_d_sparse_elem
from .mathStructs import Imsl_d_sparse_elem

IMSL_A_TRANSPOSE = 11145
IMSL_B_TRANSPOSE = 11146
imslmath = loadimsl(MATH)


def matAddCoordinate(n, alpha, a, beta, b, nzC, aTranspose=None, bTranspose=None):
    """ Performs element-wise addition on two real matrices stored in coordinate format.
    """
    imslmath.imsl_d_mat_add_coordinate.restype = POINTER(Imsl_d_sparse_elem)
    shape = []
    evalstring = 'imslmath.imsl_d_mat_add_coordinate('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nzA)'
    evalstring += ','
    evalstring += 'c_double(alpha)'
    evalstring += ','
    a_tmp = toNumpyArray(a, 'a', shape=shape,
                         dtype='Imsl_d_sparse_elem', expectedShape=(0, 0))
    #    a = toNumpyArray(a, 'a', shape=shape, dtype='struct', expectedShape=(0))
    #    evalstring +='a'
    #    nzA=shape[0]
    evalstring += 'a_tmp'
    nzA = len(a)
    evalstring += ','
    evalstring += 'c_int(nzB)'
    evalstring += ','
    evalstring += 'c_double(beta)'
    evalstring += ','
    b_tmp = toNumpyArray(b, 'b', shape=shape,
                         dtype='Imsl_d_sparse_elem', expectedShape=(0, 0))
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
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if isinstance(nzC, list):
        nzC[:] = []
    processRet(nzC_tmp, shape=1, pyvar=nzC)
    res = []
    for i in range(0, nzC[0]):
        temp = result[i].val
        res.append([result[i].row, result[i].col, result[i].val])
    return res
