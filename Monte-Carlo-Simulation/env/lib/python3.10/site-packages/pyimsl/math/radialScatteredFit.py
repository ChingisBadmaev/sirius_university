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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForCallable, checkForList, checkForDict, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_radial_basis_fit
IMSL_CENTERS = 11065
IMSL_CENTERS_RATIO = 11066
IMSL_RANDOM_SEED = 11068
IMSL_SUPPLY_BASIS = 11062
IMSL_SUPPLY_BASIS_W_DATA = 13112
IMSL_SUPPLY_DELTA = 11063
IMSL_WEIGHTS = 10141
IMSL_NO_SVD = 11081
imslmath = loadimsl(MATH)


def radialScatteredFit(abscissae, fdata, numCenters, centers=None, centersRatio=None, randomSeed=None, supplyBasis=None, supplyBasisWData=None, supplyDelta=None, weights=None, noSvd=None):
    """ Computes an approximation to scattered data in Rn for n = 1 using radial-basis functions.
    """
    imslmath.imsl_d_radial_scattered_fit.restype = POINTER(
        Imsl_d_radial_basis_fit)
    shape = []
    evalstring = 'imslmath.imsl_d_radial_scattered_fit('
    evalstring += 'c_int(dimension)'
    evalstring += ','
    evalstring += 'c_int(numPoints)'
    evalstring += ','
    abscissae = toNumpyArray(abscissae, 'abscissae',
                             shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'abscissae.ctypes.data_as(c_void_p)'
    if shape[1] == 1:
        dimension = 1
        numPoints = shape[0]
    else:
        numPoints = shape[0]
        dimension = shape[1]
    evalstring += ','
    fdata = toNumpyArray(fdata, 'fdata', shape=shape,
                         dtype='double', expectedShape=(numPoints))
    evalstring += 'fdata.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(numCenters)'
    if not (centers is None):
        evalstring += ','
        evalstring += repr(IMSL_CENTERS)
        evalstring += ','
        centers = toNumpyArray(
            centers, 'centers', shape=shape, dtype='double', expectedShape=(numCenters))
        evalstring += 'centers.ctypes.data_as(c_void_p)'
    if not (centersRatio is None):
        evalstring += ','
        evalstring += repr(IMSL_CENTERS_RATIO)
        evalstring += ','
        evalstring += 'c_double(centersRatio)'
    if not (randomSeed is None):
        evalstring += ','
        evalstring += repr(IMSL_RANDOM_SEED)
        evalstring += ','
        evalstring += 'c_int(randomSeed)'
    if not (supplyBasis is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_BASIS)
        evalstring += ','
        checkForCallable(supplyBasis, 'supplyBasis')
        TMP_SUPPLYBASIS_SUPPLYBASIS = CFUNCTYPE(c_double, c_double)
        tmp_supplyBasis_supplyBasis = TMP_SUPPLYBASIS_SUPPLYBASIS(supplyBasis)
        evalstring += 'tmp_supplyBasis_supplyBasis'
    if not (supplyBasisWData is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_BASIS_W_DATA)
        checkForDict(supplyBasisWData, 'supplyBasisWData',
                     ['radial_function', 'data'])
        evalstring += ','
        tmp_supplyBasisWData_supplyBasisWData_param = supplyBasisWData['radial_function']
        checkForCallable(
            tmp_supplyBasisWData_supplyBasisWData_param, 'supplyBasisWData')
        TMP_SUPPLYBASISWDATA_SUPPLYBASISWDATA = CFUNCTYPE(
            c_double, c_double, POINTER(c_double))
        tmp_supplyBasisWData_supplyBasisWData = TMP_SUPPLYBASISWDATA_SUPPLYBASISWDATA(
            tmp_supplyBasisWData_supplyBasisWData_param)
        evalstring += 'tmp_supplyBasisWData_supplyBasisWData'
        evalstring += ','
        supplyBasisWData_data_tmp = supplyBasisWData['data']
        supplyBasisWData_data_tmp = toNumpyArray(
            supplyBasisWData_data_tmp, 'data', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'supplyBasisWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (supplyDelta is None):
        evalstring += ','
        evalstring += repr(IMSL_SUPPLY_DELTA)
        evalstring += ','
        evalstring += 'c_double(supplyDelta)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(numPoints))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    checkForBoolean(noSvd, 'noSvd')
    if (noSvd):
        evalstring += ','
        evalstring += repr(IMSL_NO_SVD)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    state = [result]
    if not (supplyBasis is None):
        state.append(tmp_supplyBasis_supplyBasis)

    return state
