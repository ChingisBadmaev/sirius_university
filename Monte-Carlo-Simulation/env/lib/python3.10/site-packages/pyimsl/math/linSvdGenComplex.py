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
from pyimsl.util.imslUtils import MATH, checkForList, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import dtype, min, rank, shape, size
from ctypes import POINTER, byref, c_double, c_int
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex
from .mathStructs import d_complex

IMSL_RANK = 10049
IMSL_U = 10199
IMSL_V = 10202
IMSL_INVERSE = 10152
imslmath = loadimsl(MATH)


def linSvdGenComplex(a, rank=None, u=None, v=None, inverse=None):
    """ Computes the SVD, A = USVH, of a complex rectangular matrix A. An approximate generalized inverse and rank of A also can be computed.
    """
    imslmath.imsl_z_lin_svd_gen.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_lin_svd_gen('
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='d_complex',
                     expectedShape=(0, 0))
    evalstring += 'a'
    m = shape[0]
    n = shape[1]
    if n < m:
        retSize = n
    else:
        retSize = m
    if not (rank is None):
        evalstring += ','
        evalstring += repr(IMSL_RANK)
        checkForDict(rank, 'rank', ['tol'])
        evalstring += ','
        rank_tol_tmp = rank['tol']
        evalstring += 'c_double(rank_tol_tmp)'
        evalstring += ','
        rank_rank_tmp = c_int()
        if 'rank' in rank:  # rank is input/output so not always defined on output
            rank_rank_tmp = c_int(rank['rank'])
        evalstring += 'byref(rank_rank_tmp)'
    if not (u is None):
        evalstring += ','
        evalstring += repr(IMSL_U)
        checkForList(u, 'u')
        evalstring += ','
        u_pU_tmp = POINTER(d_complex)(d_complex())
        evalstring += 'byref(u_pU_tmp)'
    if not (v is None):
        evalstring += ','
        evalstring += repr(IMSL_V)
        checkForList(v, 'v')
        evalstring += ','
        v_pV_tmp = POINTER(d_complex)(d_complex())
        evalstring += 'byref(v_pV_tmp)'
    if not (inverse is None):
        evalstring += ','
        evalstring += repr(IMSL_INVERSE)
        checkForList(inverse, 'inverse')
        evalstring += ','
        inverse_pGenInva_tmp = POINTER(d_complex)(d_complex())
        evalstring += 'byref(inverse_pGenInva_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (rank is None):
        processRet(rank_rank_tmp, shape=(1), key='rank', pyvar=rank)
    if not (u is None):
        processRet(u_pU_tmp, shape=(m, retSize), pyvar=u)
    if not (v is None):
        processRet(v_pV_tmp, shape=(n, n), pyvar=v)
    if not (inverse is None):
        processRet(inverse_pGenInva_tmp, shape=(n, m), pyvar=inverse)
    procRet = processRet(result, shape=(retSize), result=True)
    return procRet
