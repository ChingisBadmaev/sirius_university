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
from pyimsl.util.imslUtils import Imsl_c_sparse_elem, MATH, checkForBoolean, checkForList, checkForDict, checkForStr, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray, toByte
from numpy import any, complex, dtype, int, matrix, shape, single, size
from ctypes import POINTER, byref, c_int, pointer
from .mathStructs import d_complex
from pyimsl.util.Translator import Translator

IMSL_A_MATRIX = 10181
IMSL_B_MATRIX = 10182
IMSL_X_VECTOR = 10183
IMSL_RETURN_MATRIX_SIZE = 11114
IMSL_SYMMETRIC_STORAGE = 11094
imslmath = loadimsl(MATH)


def matMulRectCoordinateComplex(string, aMatrix=None, bMatrix=None, xVector=None, returnMatrixSize=None, sparseOutput=None, symmetricStorage=None):
    """Computes the transpose of a matrix, a matrix-vector produce, or a matrix-matrix product for all matrices stored in sparse coordinate form.
    """
    # The size and datatype of the returned matrix are determined by
    # the contents of the input string.  I couldn't find any easy
    # way to determine either of these quantities for this routine,
    # so I'm going to leave it unimplimented for the time being.
    #
    # raise NotImplementedError, "matMulRectCoordinateComplex is not implemented."

    # There is not really a good way to figure out when this function might
    # return a pointer to sparese_elem or float.  For right now, users must tell
    # us when they expect to get a sparse output by setting the sparseOutput=true
    if sparseOutput:
        imslmath.imsl_z_mat_mul_rect_coordinate.restype = POINTER(
            Imsl_c_sparse_elem)
    else:
        imslmath.imsl_z_mat_mul_rect_coordinate.restype = POINTER(d_complex)

    # imslmath.imsl_z_mat_mul_rect_coordinate.restype = None
    shape = []
    evalstring = 'imslmath.imsl_z_mat_mul_rect_coordinate('
    checkForStr(string, 'string')
    evalstring += 'toByte(string)'
    # use the size that is provided by the x vector and not by the user.  The
    # nsize keyword is mostly needed when users might use a single argument in
    # the input string.  for example, string = "x"
    if not (xVector is None):
        xVector_x_tmp = toNumpyArray(
            xVector, 'xVector', shape=shape, dtype='d_complex', expectedShape=(0))
        nsize = shape[0]
    if not (aMatrix is None):
        evalstring += ','
        evalstring += repr(IMSL_A_MATRIX)
        checkForDict(aMatrix, 'aMatrix', ['nrowa', 'ncola', 'a'])
        evalstring += ','
        aMatrix_nrowa_tmp = aMatrix['nrowa']
        evalstring += 'c_int(aMatrix_nrowa_tmp)'
        evalstring += ','
        aMatrix_ncola_tmp = aMatrix['ncola']
        if (aMatrix_nrowa_tmp != aMatrix_ncola_tmp):
            errStr = Translator.getString("unequalRowsCols")
            raise ValueError(errStr)
        evalstring += 'c_int(aMatrix_ncola_tmp)'
        evalstring += ','
        aMatrix_a_tmp = aMatrix['a']
        aMatrix_nza_tmp = len(aMatrix_a_tmp)
        evalstring += 'c_int(aMatrix_nza_tmp)'
        evalstring += ','
        aMatrix_a_tmp = toNumpyArray(
            aMatrix_a_tmp, 'aMatrix', shape=shape, dtype='Imsl_c_sparse_elem', expectedShape=(0, 0))
        evalstring += 'aMatrix_a_tmp'
        nsize = aMatrix_nrowa_tmp
    if not (bMatrix is None):
        evalstring += ','
        evalstring += repr(IMSL_B_MATRIX)
        checkForDict(bMatrix, 'bMatrix', ['nrowb', 'ncolb', 'b'])
        evalstring += ','
        bMatrix_nrowb_tmp = bMatrix['nrowb']
        evalstring += 'c_int(bMatrix_nrowb_tmp)'
        evalstring += ','
        bMatrix_ncolb_tmp = bMatrix['ncolb']
        if (bMatrix_nrowa_tmp != bMatrix_ncola_tmp):
            errStr = Translator.getString("unequalRowsCols")
            raise ValueError(errStr)
        evalstring += 'c_int(bMatrix_ncolb_tmp)'
        evalstring += ','
        bMatrix_b_tmp = bMatrix['b']
        bMatrix_nzb_tmp = len(bMatrix_b_tmp)
        evalstring += 'c_int(bMatrix_nzb_tmp)'
        evalstring += ','
        bMatrix_b_tmp = toNumpyArray(
            bMatrix_b_tmp, 'bMatrix', shape=shape, dtype='Imsl_c_sparse_elem', expectedShape=(0, 0))
        evalstring += 'bMatrix_b_tmp'
        nsize = bMatrix_nrowb_tmp
    if not (xVector is None):
        evalstring += ','
        evalstring += repr(IMSL_X_VECTOR)
        evalstring += ','
        evalstring += 'c_int(xVector_nx_tmp)'
        evalstring += ','
        xVector_x_tmp = toNumpyArray(
            xVector, 'xVector', shape=shape, dtype='d_complex', expectedShape=(0))
        evalstring += 'xVector_x_tmp'
        xVector_nx_tmp = shape[0]
    if not (returnMatrixSize is None):
        evalstring += ','
        evalstring += repr(IMSL_RETURN_MATRIX_SIZE)
        checkForList(returnMatrixSize, 'returnMatrixSize')
        evalstring += ','
        returnMatrixSize_size_tmp = c_int()
        evalstring += 'byref(returnMatrixSize_size_tmp)'
    checkForBoolean(symmetricStorage, 'symmetricStorage')
    if (symmetricStorage):
        evalstring += ','
        evalstring += repr(IMSL_SYMMETRIC_STORAGE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (returnMatrixSize is None):
        processRet(returnMatrixSize_size_tmp, shape=1, pyvar=returnMatrixSize)
    if sparseOutput:
        # result is a pointer to Imsl_c_sparse_elem.
        # Imsl_c_sparse struct is made up of row,col, and value
        # but the value is of type d_complex (imsl struct), we need
        # to convert it back to python complex.
        # We can make use of the list to hold both int for rows/cols and complex
        # values.
        res = []
        for i in range(0, returnMatrixSize[0]):
            temp = result[i].val
            res.append([result[i].row, result[i].col,
                        (complex(temp.re, temp.im))])
    else:  # d_complex
        res = processRet(result, shape=((nsize)), result=True)
    return res
