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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_regression

IMSLS_GP = 20945
IMSLS_U = 15180
IMSLS_RANK_HP = 20946
IMSLS_H_MATRIX = 20948
IMSLS_G = 20943
imslstat = loadimsl(STAT)


def hypothesisPartial(regressionInfo, hp, gp=None, u=None, rankHp=None, hMatrix=None, g=None):
    """ Constructs an equivalent completely testable multivariate general linear hypothesis from a partially testable hypothesis.
    """
    imslstat.imsls_d_hypothesis_partial.restype = c_int
    shape = []
    evalstring = 'imslstat.imsls_d_hypothesis_partial('
    evalstring += 'regressionInfo'
    evalstring += ','
    evalstring += 'c_int(nhp)'
    evalstring += ','
    hp = toNumpyArray(hp, 'hp', shape=shape,
                      dtype='double', expectedShape=(0, 0))
    evalstring += 'hp.ctypes.data_as(c_void_p)'
    nhp = shape[0]
    if not (gp is None):
        evalstring += ','
        evalstring += repr(IMSLS_GP)
        evalstring += ','
        gp = toNumpyArray(gp, 'gp', shape=shape,
                          dtype='double', expectedShape=(nhp, 0))
        evalstring += 'gp.ctypes.data_as(c_void_p)'
    if not (u is None):
        evalstring += ','
        evalstring += repr(IMSLS_U)
        checkForList(u, 'u', size=1)
        evalstring += ','
        evalstring += 'c_int(u_nu_tmp)'
        evalstring += ','
        u_u_tmp = toNumpyArray(u, 'u', shape=shape, dtype='double', expectedShape=(
            regressionInfo[0].nDependent, 0))
        evalstring += 'u_u_tmp.ctypes.data_as(c_void_p)'
        u_nu_tmp = shape[1]
    if not (rankHp is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANK_HP)
        checkForList(rankHp, 'rankHp')
        evalstring += ','
        rankHp_rankHp_tmp = c_int()
        evalstring += 'byref(rankHp_rankHp_tmp)'
    if not (hMatrix is None):
        evalstring += ','
        evalstring += repr(IMSLS_H_MATRIX)
        checkForList(hMatrix, 'hMatrix')
        evalstring += ','
        hMatrix_h_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(hMatrix_h_tmp)'
    if not (g is None):
        evalstring += ','
        evalstring += repr(IMSLS_G)
        checkForList(g, 'g')
        evalstring += ','
        g_g_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(g_g_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (rankHp is None):
        processRet(rankHp_rankHp_tmp, shape=(1), pyvar=rankHp)

    # NOTE: The documentation says the size of G and H are nhp by n_parameters,
    # but the example and the text seem to imply that it should be
    # nh by n_parameters.  I'm going to file this as a bug and
    # use nh for the first dimension.
    nh = result
    if not (hMatrix is None):
        #        processRet(hMatrix_h_tmp, shape=(nhp,regressionInfo[0].n_parameters), pyvar=hMatrix)
        processRet(hMatrix_h_tmp, shape=(
            nh, regressionInfo[0].n_parameters), pyvar=hMatrix)
    if not (g is None):
        #        processRet(g_g_tmp, shape=(nhp,regressionInfo[0].n_dependent), pyvar=g)
        processRet(g_g_tmp, shape=(nh, regressionInfo[0].n_dependent), pyvar=g)
    return result
