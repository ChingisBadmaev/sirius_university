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
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_PRINT = 13900
IMSLS_ERR_ABS = 11440
IMSLS_ERR_REL = 11490
IMSLS_TOLERANCE = 15040
IMSLS_MAX_EVALS = 12930
IMSLS_RANDOM_SEED = 50600
IMSLS_ERR_EST = 11460
imslstat = loadimsl(STAT)


def multivariateNormalCdf(h, mean, sigma, t_print=None, errAbs=None, errRel=None, tolerance=None, maxEvals=None, randomSeed=None, errEst=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_multivariate_normal_cdf.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_multivariate_normal_cdf('
    evalstring += 'c_int(k)'
    evalstring += ','
    h = toNumpyArray(h, 'h', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'h.ctypes.data_as(c_void_p)'
    k = shape[0]
    evalstring += ','
    mean = toNumpyArray(mean, 'mean', shape=shape,
                        dtype='double', expectedShape=(k))
    evalstring += 'mean.ctypes.data_as(c_void_p)'
    evalstring += ','
    sigma = toNumpyArray(sigma, 'sigma', shape=shape,
                         dtype='double', expectedShape=(k, k))
    evalstring += 'sigma.ctypes.data_as(c_void_p)'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    if not (errAbs is None):
        evalstring += ','
        evalstring += repr(IMSLS_ERR_ABS)
        evalstring += ','
        evalstring += 'c_double(errAbs)'
    if not (errRel is None):
        evalstring += ','
        evalstring += repr(IMSLS_ERR_REL)
        evalstring += ','
        evalstring += 'c_double(errRel)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (maxEvals is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_EVALS)
        evalstring += ','
        evalstring += 'c_int(maxEvals)'
    if not (randomSeed is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANDOM_SEED)
        evalstring += ','
        evalstring += 'c_int(randomSeed)'
    if not (errEst is None):
        evalstring += ','
        evalstring += repr(IMSLS_ERR_EST)
        checkForList(errEst, 'errEst')
        evalstring += ','
        errEst_errEst_tmp = c_double()
        evalstring += 'byref(errEst_errEst_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (errEst is None):
        processRet(errEst_errEst_tmp, shape=(1), pyvar=errEst)
    return result
