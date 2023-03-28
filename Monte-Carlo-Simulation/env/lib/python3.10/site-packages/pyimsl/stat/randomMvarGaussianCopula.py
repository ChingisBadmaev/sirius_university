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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *

imslstat = loadimsl(STAT)


def randomMvarGaussianCopula(chol):
    """ Given a Cholesky factorization of a correlation matrix, generates pseudorandom numbers from a Gaussian Copula distribution.
    """
    imslstat.imsls_d_random_mvar_gaussian_copula.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_random_mvar_gaussian_copula('
    evalstring += 'c_int(n)'
    evalstring += ','
    chol = toNumpyArray(chol, 'chol', shape=shape,
                        dtype='double', expectedShape=(0, 0))
    evalstring += 'chol.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(n), result=True)
