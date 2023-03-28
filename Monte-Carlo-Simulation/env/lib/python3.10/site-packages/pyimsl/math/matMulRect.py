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
from pyimsl.util.imslUtils import MATH, checkForStr, fatalErrorCheck, loadimsl, processRet, toNumpyArray, toByte
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p
from .matMulResultSize import matMulResultSize

IMSL_A_MATRIX = 10181
IMSL_A_COL_DIM = 10003
IMSL_B_MATRIX = 10182
IMSL_B_COL_DIM = 10186
IMSL_X_VECTOR = 10183
IMSL_Y_VECTOR = 10184
IMSL_RETURN_COL_DIM = 10185
imslmath = loadimsl(MATH)


def matMulRect(string, aMatrix=None, aColDim=None, bMatrix=None, bColDim=None, xVector=None, yVector=None, returnColDim=None):
    """ Computes the transpose of a matrix, a matrix-vector product, a matrix-matrix product, the bilinear form, or any triple product.
    """
    imslmath.imsl_d_mat_mul_rect.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_mat_mul_rect('
    checkForStr(string, 'string')
    evalstring += 'toByte(string)'
    aMatrix_nrowa_tmp = 1
    aMatrix_ncola_tmp = 1
    bMatrix_nrowb_tmp = 1
    bMatrix_ncolb_tmp = 1
    xVector_nx_tmp = 1
    yVector_ny_tmp = 1
    if not (aMatrix is None):
        evalstring += ','
        evalstring += repr(IMSL_A_MATRIX)
        evalstring += ','
        evalstring += 'c_int(aMatrix_nrowa_tmp)'
        evalstring += ','
        evalstring += 'c_int(aMatrix_ncola_tmp)'
        evalstring += ','
        aMatrix_a_tmp = toNumpyArray(
            aMatrix, 'aMatrix', shape=shape, dtype='double', expectedShape=(0, 0))
        evalstring += 'aMatrix_a_tmp.ctypes.data_as(c_void_p)'
        aMatrix_nrowa_tmp = shape[0]
        aMatrix_ncola_tmp = shape[1]
    if not (aColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_A_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(aColDim)'
    if not (bMatrix is None):
        evalstring += ','
        evalstring += repr(IMSL_B_MATRIX)
        evalstring += ','
        evalstring += 'c_int(bMatrix_nrowb_tmp)'
        evalstring += ','
        evalstring += 'c_int(bMatrix_ncolb_tmp)'
        evalstring += ','
        bMatrix_b_tmp = toNumpyArray(
            bMatrix, 'bMatrix', shape=shape, dtype='double', expectedShape=(0, 0))
        evalstring += 'bMatrix_b_tmp.ctypes.data_as(c_void_p)'
        bMatrix_nrowb_tmp = shape[0]
        bMatrix_ncolb_tmp = shape[1]
    if not (bColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_B_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(bColDim)'
    if not (xVector is None):
        evalstring += ','
        evalstring += repr(IMSL_X_VECTOR)
        evalstring += ','
        evalstring += 'c_int(xVector_nx_tmp)'
        evalstring += ','
        xVector_x_tmp = toNumpyArray(
            xVector, 'xVector', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'xVector_x_tmp.ctypes.data_as(c_void_p)'
        xVector_nx_tmp = shape[0]
    if not (yVector is None):
        evalstring += ','
        evalstring += repr(IMSL_Y_VECTOR)
        evalstring += ','
        evalstring += 'c_int(yVector_ny_tmp)'
        evalstring += ','
        yVector_y_tmp = toNumpyArray(
            yVector, 'yVector', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'yVector_y_tmp.ctypes.data_as(c_void_p)'
        yVector_ny_tmp = shape[0]
    if not (returnColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(returnColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)

    resultSize = matMulResultSize(string, aMatrix_nrowa_tmp, aMatrix_ncola_tmp,
                                  bMatrix_nrowb_tmp, bMatrix_ncolb_tmp, xVector_nx_tmp, yVector_ny_tmp)
    return processRet(result, shape=(resultSize[0], resultSize[1]), result=True)
