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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, gradient, int, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_NN_Network

# Weight initialization methods
EQUAL = 1
RANDOM = 2
PRINCIPAL_COMPONENTS = 3
DISCRIMINANT = 4

IMSLS_STAGE_I = 40609
IMSLS_NO_STAGE_II = 40610
IMSLS_MAX_STEP = 13070
IMSLS_MAX_ITN = 12980
IMSLS_MAX_FCN = 12940
IMSLS_REL_FCN_TOL = 14170
IMSLS_GRAD_TOL = 12070
IMSLS_TOLERANCE = 15040
IMSLS_PRINT = 13900
IMSLS_RESIDUAL = 14190
IMSLS_GRADIENT = 12050
IMSLS_FORECASTS = 25730
IMSLS_WEIGHT_INITIALIZATION_METHOD = 40616

imslstat = loadimsl(STAT)


def mlffNetworkTrainer(network, nominal, continuous, output, stageI=None, noStageIi=None, maxStep=None, maxItn=None, maxFcn=None, relFcnTol=None, gradTol=None, tolerance=None, weightInitializationMethod=None, t_print=None, residual=None, gradient=None, forecasts=None):
    """ Trains a multilayered feedforward neural network.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_mlff_network_trainer.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_network_trainer('
    evalstring += 'network'
    evalstring += ','
    evalstring += 'c_int(nPatterns)'
    evalstring += ','
    evalstring += 'c_int(nNominal)'
    evalstring += ','
    evalstring += 'c_int(nContinuous)'
    evalstring += ','
    if (nominal is None):
        nPatterns = 0
        nNominal = 0
        evalstring += 'None'
    else:
        nominal = toNumpyArray(
            nominal, 'nominal', shape=shape, dtype='int', expectedShape=(0, 0))
        nPatterns = shape[0]
        nNominal = shape[1]
        evalstring += 'nominal.ctypes.data_as(c_void_p)'
    evalstring += ','
    if (continuous is None):
        nContinuous = 0
        evalstring += 'None'
    else:
        continuous = toNumpyArray(
            continuous, 'continuous', shape=shape, dtype='double', expectedShape=(nPatterns, 0))
        if (nPatterns == 0):
            nPatterns = shape[0]
        nContinuous = shape[1]
        evalstring += 'continuous.ctypes.data_as(c_void_p)'
    evalstring += ','
    # ++Custom code
    layerNum = network[0].n_layers - 1
    nLinks = network[0].n_links
    nNodes = network[0].n_nodes
    ver = VersionFacade.getCnlVersion()
    if (ver.majorVersion >= 7):
        nInputs = network[0].n_inputs
        nOutputs = network[0].n_outputs
    else:
        nInputs = network[0].layers[0].nodes
        nOutputs = network[0].layers[layerNum].n_nodes
    # --Custom code
    output = toNumpyArray(output, 'output', shape=shape,
                          dtype='double', expectedShape=(nPatterns, nOutputs))
    evalstring += 'output.ctypes.data_as(c_void_p)'
    if not (stageI is None):
        evalstring += ','
        evalstring += repr(IMSLS_STAGE_I)
        checkForDict(stageI, 'stageI', ['nEpochs', 'epochSize'])
        evalstring += ','
        stageI_nEpochs_tmp = stageI['nEpochs']
        evalstring += 'c_int(stageI_nEpochs_tmp)'
        evalstring += ','
        stageI_epochSize_tmp = stageI['epochSize']
        evalstring += 'c_int(stageI_epochSize_tmp)'
    checkForBoolean(noStageIi, 'noStageIi')
    if (noStageIi):
        evalstring += ','
        evalstring += repr(IMSLS_NO_STAGE_II)
    if not (maxStep is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_STEP)
        evalstring += ','
        evalstring += 'c_double(maxStep)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    if not (relFcnTol is None):
        evalstring += ','
        evalstring += repr(IMSLS_REL_FCN_TOL)
        evalstring += ','
        evalstring += 'c_double(relFcnTol)'
    if not (gradTol is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRAD_TOL)
        evalstring += ','
        evalstring += 'c_double(gradTol)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (weightInitializationMethod is None):
        VersionFacade.checkVersion(7)
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHT_INITIALIZATION_METHOD)
        evalstring += ','
        evalstring += 'c_int(weightInitializationMethod)'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSLS_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residuals_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residuals_tmp)'
    if not (gradient is None):
        evalstring += ','
        evalstring += repr(IMSLS_GRADIENT)
        checkForList(gradient, 'gradient')
        evalstring += ','
        gradient_gradients_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(gradient_gradients_tmp)'
    if not (forecasts is None):
        evalstring += ','
        evalstring += repr(IMSLS_FORECASTS)
        checkForList(forecasts, 'forecasts')
        evalstring += ','
        forecasts_forecasts_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(forecasts_forecasts_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (residual is None):
        processRet(residual_residuals_tmp, shape=(
            nPatterns, nOutputs), pyvar=residual)
    if not (gradient is None):
        processRet(gradient_gradients_tmp, shape=(
            nLinks + nNodes - nInputs), pyvar=gradient)
    if not (forecasts is None):
        processRet(forecasts_forecasts_tmp, shape=(
            nPatterns, nOutputs), pyvar=forecasts)
    return processRet(result, shape=(5), result=True)
