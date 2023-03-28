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
from numpy import double, dtype, power, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_MAXIMUM_LIKELIHOOD = 12900
IMSLS_PRINCIPAL_COMPONENT = 13890
IMSLS_PRINCIPAL_FACTOR = 13880
IMSLS_UNWEIGHTED_LEAST_SQUARES = 15240
IMSLS_GENERALIZED_LEAST_SQUARES = 11940
IMSLS_IMAGE = 12280
IMSLS_ALPHA = 10070
IMSLS_UNIQUE_VARIANCES_INPUT = 15210
IMSLS_UNIQUE_VARIANCES_OUTPUT = 15220
IMSLS_MAX_ITERATIONS = 12970
IMSLS_MAX_STEPS_LINE_SEARCH = 13080
IMSLS_CONVERGENCE_EPS = 10980
IMSLS_SWITCH_EXACT_HESSIAN = 14920
IMSLS_EIGENVALUES = 11300
IMSLS_CHI_SQUARED_TEST = 10510
IMSLS_TUCKER_RELIABILITY_COEFFICIENT = 15080
IMSLS_N_ITERATIONS = 13430
IMSLS_FUNCTION_MIN = 11860
IMSLS_LAST_STEP = 12680
IMSLS_ORTHOMAX_ROTATION = 40320
IMSLS_ORTHOGONAL_PROCRUSTES_ROTATION = 40322
IMSLS_DIRECT_OBLIMIN_ROTATION = 40324
IMSLS_OBLIQUE_PROMAX_ROTATION = 40326
IMSLS_OBLIQUE_PIVOTAL_PROMAX_ROTATION = 40328
IMSLS_OBLIQUE_PROCRUSTES_ROTATION = 40330
IMSLS_FACTOR_STRUCTURE = 40332
IMSLS_COV_COL_DIM = 11055
imslstat = loadimsl(STAT)


def factorAnalysis(covariances, nFactors, maximumLikelihood=None, principalComponent=None, principalFactor=None, unweightedLeastSquares=None, generalizedLeastSquares=None, image=None, alpha=None, uniqueVariancesInput=None, uniqueVariancesOutput=None, maxIterations=None, maxStepsLineSearch=None, convergenceEps=None, switchExactHessian=None, eigenvalues=None, chiSquaredTest=None, tuckerReliabilityCoefficient=None, nIterations=None, functionMin=None, lastStep=None, orthomaxRotation=None, orthogonalProcrustesRotation=None, directObliminRotation=None, obliquePromaxRotation=None, obliquePivotalPromaxRotation=None, obliqueProcrustesRotation=None, factorStructure=None, covColDim=None):
    """ Extracts initial factor-loading estimates in factor analysis with rotation options.
    """
    imslstat.imsls_d_factor_analysis.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_factor_analysis('
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    covariances = toNumpyArray(
        covariances, 'covariances', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'covariances.ctypes.data_as(c_void_p)'
    nVariables = shape[0]
    evalstring += ','
    evalstring += 'c_int(nFactors)'
    if not (maximumLikelihood is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAXIMUM_LIKELIHOOD)
        evalstring += ','
        evalstring += 'c_int(maximumLikelihood)'
    checkForBoolean(principalComponent, 'principalComponent')
    if (principalComponent):
        evalstring += ','
        evalstring += repr(IMSLS_PRINCIPAL_COMPONENT)
    checkForBoolean(principalFactor, 'principalFactor')
    if (principalFactor):
        evalstring += ','
        evalstring += repr(IMSLS_PRINCIPAL_FACTOR)
    checkForBoolean(unweightedLeastSquares, 'unweightedLeastSquares')
    if (unweightedLeastSquares):
        evalstring += ','
        evalstring += repr(IMSLS_UNWEIGHTED_LEAST_SQUARES)
    if not (generalizedLeastSquares is None):
        evalstring += ','
        evalstring += repr(IMSLS_GENERALIZED_LEAST_SQUARES)
        evalstring += ','
        evalstring += 'c_int(generalizedLeastSquares)'
    checkForBoolean(image, 'image')
    if (image):
        evalstring += ','
        evalstring += repr(IMSLS_IMAGE)
    if not (alpha is None):
        evalstring += ','
        evalstring += repr(IMSLS_ALPHA)
        evalstring += ','
        evalstring += 'c_int(alpha)'
    if not (uniqueVariancesInput is None):
        evalstring += ','
        evalstring += repr(IMSLS_UNIQUE_VARIANCES_INPUT)
        evalstring += ','
        uniqueVariancesInput = toNumpyArray(
            uniqueVariancesInput, 'uniqueVariancesInput', shape=shape, dtype='double', expectedShape=(nVariables))
        evalstring += 'uniqueVariancesInput.ctypes.data_as(c_void_p)'
    if not (uniqueVariancesOutput is None):
        evalstring += ','
        evalstring += repr(IMSLS_UNIQUE_VARIANCES_OUTPUT)
        checkForList(uniqueVariancesOutput, 'uniqueVariancesOutput')
        evalstring += ','
        # user allocated array
        uniqueVariancesOutput_uniqueVariancesOutput_tmp = toNumpyArray(
            uniqueVariancesOutput, 'uniqueVariancesOutput', shape=shape, dtype='double', expectedShape=(nVariables))
        evalstring += 'uniqueVariancesOutput_uniqueVariancesOutput_tmp.ctypes.data_as(c_void_p)'
        # uniqueVariancesOutput_uniqueVariancesOutput_tmp = POINTER(c_double)(c_double())
        # evalstring += 'byref(uniqueVariancesOutput_uniqueVariancesOutput_tmp)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (maxStepsLineSearch is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_STEPS_LINE_SEARCH)
        evalstring += ','
        evalstring += 'c_int(maxStepsLineSearch)'
    if not (convergenceEps is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONVERGENCE_EPS)
        evalstring += ','
        evalstring += 'c_double(convergenceEps)'
    if not (switchExactHessian is None):
        evalstring += ','
        evalstring += repr(IMSLS_SWITCH_EXACT_HESSIAN)
        evalstring += ','
        evalstring += 'c_double(switchExactHessian)'
    if not (eigenvalues is None):
        evalstring += ','
        evalstring += repr(IMSLS_EIGENVALUES)
        checkForList(eigenvalues, 'eigenvalues')
        evalstring += ','
        eigenvalues_eigenvalues_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(eigenvalues_eigenvalues_tmp)'
    if not (chiSquaredTest is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED_TEST)
        checkForDict(chiSquaredTest, 'chiSquaredTest', [])
        evalstring += ','
        chiSquaredTest_df_tmp = c_int()
        evalstring += 'byref(chiSquaredTest_df_tmp)'
        evalstring += ','
        chiSquaredTest_chiSquared_tmp = c_double()
        evalstring += 'byref(chiSquaredTest_chiSquared_tmp)'
        evalstring += ','
        chiSquaredTest_pValue_tmp = c_double()
        evalstring += 'byref(chiSquaredTest_pValue_tmp)'
    if not (tuckerReliabilityCoefficient is None):
        evalstring += ','
        evalstring += repr(IMSLS_TUCKER_RELIABILITY_COEFFICIENT)
        checkForList(tuckerReliabilityCoefficient,
                     'tuckerReliabilityCoefficient')
        evalstring += ','
        tuckerReliabilityCoefficient_tuckerReliabilityCoefficient_tmp = c_double()
        evalstring += 'byref(tuckerReliabilityCoefficient_tuckerReliabilityCoefficient_tmp)'
    if not (nIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_ITERATIONS)
        checkForList(nIterations, 'nIterations')
        evalstring += ','
        nIterations_nIterations_tmp = c_int()
        evalstring += 'byref(nIterations_nIterations_tmp)'
    if not (functionMin is None):
        evalstring += ','
        evalstring += repr(IMSLS_FUNCTION_MIN)
        checkForList(functionMin, 'functionMin')
        evalstring += ','
        functionMin_functionMin_tmp = c_double()
        evalstring += 'byref(functionMin_functionMin_tmp)'
    if not (lastStep is None):
        evalstring += ','
        evalstring += repr(IMSLS_LAST_STEP)
        checkForList(lastStep, 'lastStep')
        evalstring += ','
        lastStep_lastStep_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(lastStep_lastStep_tmp)'
    if not (orthomaxRotation is None):
        evalstring += ','
        evalstring += repr(IMSLS_ORTHOMAX_ROTATION)
        checkForDict(orthomaxRotation, 'orthomaxRotation', ['w', 'norm'])
        evalstring += ','
        orthomaxRotation_w_tmp = orthomaxRotation['w']
        evalstring += 'c_double(orthomaxRotation_w_tmp)'
        evalstring += ','
        orthomaxRotation_norm_tmp = orthomaxRotation['norm']
        evalstring += 'c_int(orthomaxRotation_norm_tmp)'
        evalstring += ','
        orthomaxRotation_b_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(orthomaxRotation_b_tmp)'
        evalstring += ','
        orthomaxRotation_t_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(orthomaxRotation_t_tmp)'
    if not (orthogonalProcrustesRotation is None):
        evalstring += ','
        evalstring += repr(IMSLS_ORTHOGONAL_PROCRUSTES_ROTATION)
        checkForDict(orthogonalProcrustesRotation,
                     'orthogonalProcrustesRotation', ['target'])
        evalstring += ','
        orthogonalProcrustesRotation_target_tmp = orthogonalProcrustesRotation['target']
        orthogonalProcrustesRotation_target_tmp = toNumpyArray(
            orthogonalProcrustesRotation_target_tmp, 'target', shape=shape, dtype='double', expectedShape=(nVariables, nFactors))
        evalstring += 'orthogonalProcrustesRotation_target_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        orthogonalProcrustesRotation_b_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(orthogonalProcrustesRotation_b_tmp)'
        evalstring += ','
        orthogonalProcrustesRotation_t_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(orthogonalProcrustesRotation_t_tmp)'
    if not (directObliminRotation is None):
        evalstring += ','
        evalstring += repr(IMSLS_DIRECT_OBLIMIN_ROTATION)
        checkForDict(directObliminRotation,
                     'directObliminRotation', ['w', 'norm'])
        evalstring += ','
        directObliminRotation_w_tmp = directObliminRotation['w']
        evalstring += 'c_double(directObliminRotation_w_tmp)'
        evalstring += ','
        directObliminRotation_norm_tmp = directObliminRotation['norm']
        evalstring += 'c_int(directObliminRotation_norm_tmp)'
        evalstring += ','
        directObliminRotation_b_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(directObliminRotation_b_tmp)'
        evalstring += ','
        directObliminRotation_t_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(directObliminRotation_t_tmp)'
        evalstring += ','
        directObliminRotation_factorCorrelations_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(directObliminRotation_factorCorrelations_tmp)'
    if not (obliquePromaxRotation is None):
        evalstring += ','
        evalstring += repr(IMSLS_OBLIQUE_PROMAX_ROTATION)
        checkForDict(obliquePromaxRotation, 'obliquePromaxRotation', [
                     'w', 'power', 'norm', 'target', 'b', 't', 'factorCorrelations'])
        evalstring += ','
        obliquePromaxRotation_w_tmp = obliquePromaxRotation['w']
        evalstring += 'c_double(obliquePromaxRotation_w_tmp)'
        evalstring += ','
        obliquePromaxRotation_power_tmp = obliquePromaxRotation['power']
        obliquePromaxRotation_power_tmp = toNumpyArray(
            obliquePromaxRotation_power_tmp, 'power', shape=shape, dtype='double', expectedShape=(nFactors))
        evalstring += 'obliquePromaxRotation_power_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        obliquePromaxRotation_norm_tmp = obliquePromaxRotation['norm']
        evalstring += 'c_int(obliquePromaxRotation_norm_tmp)'
        evalstring += ','
        obliquePromaxRotation_target_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliquePromaxRotation_target_tmp)'
        evalstring += ','
        obliquePromaxRotation_b_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliquePromaxRotation_b_tmp)'
        evalstring += ','
        obliquePromaxRotation_t_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliquePromaxRotation_t_tmp)'
        evalstring += ','
        obliquePromaxRotation_factorCorrelations_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(obliquePromaxRotation_factorCorrelations_tmp)'
    if not (obliquePivotalPromaxRotation is None):
        evalstring += ','
        evalstring += repr(IMSLS_OBLIQUE_PIVOTAL_PROMAX_ROTATION)
        checkForDict(obliquePivotalPromaxRotation, 'obliquePivotalPromaxRotation', [
                     'w', 'pivot', 'norm', 'target', 'b', 't', 'factorCorrelations'])
        evalstring += ','
        obliquePivotalPromaxRotation_w_tmp = obliquePivotalPromaxRotation['w']
        evalstring += 'c_double(obliquePivotalPromaxRotation_w_tmp)'
        evalstring += ','
        obliquePivotalPromaxRotation_pivot_tmp = obliquePivotalPromaxRotation['pivot']
        obliquePivotalPromaxRotation_pivot_tmp = toNumpyArray(
            obliquePivotalPromaxRotation_pivot_tmp, 'pivot', shape=shape, dtype='double', expectedShape=(nFactors))
        evalstring += 'obliquePivotalPromaxRotation_pivot_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        obliquePivotalPromaxRotation_norm_tmp = obliquePivotalPromaxRotation['norm']
        evalstring += 'c_int(obliquePivotalPromaxRotation_norm_tmp)'
        evalstring += ','
        obliquePivotalPromaxRotation_target_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliquePivotalPromaxRotation_target_tmp)'
        evalstring += ','
        obliquePivotalPromaxRotation_b_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliquePivotalPromaxRotation_b_tmp)'
        evalstring += ','
        obliquePivotalPromaxRotation_t_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliquePivotalPromaxRotation_t_tmp)'
        evalstring += ','
        obliquePivotalPromaxRotation_factorCorrelations_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(obliquePivotalPromaxRotation_factorCorrelations_tmp)'
    if not (obliqueProcrustesRotation is None):
        evalstring += ','
        evalstring += repr(IMSLS_OBLIQUE_PROCRUSTES_ROTATION)
        checkForDict(obliqueProcrustesRotation,
                     'obliqueProcrustesRotation', ['target'])
        evalstring += ','
        obliqueProcrustesRotation_target_tmp = obliqueProcrustesRotation[0]
        obliqueProcrustesRotation_target_tmp = toNumpyArray(
            obliqueProcrustesRotation_target_tmp, 'target', shape=shape, dtype='double', expectedShape=(nVariables, nFactors))
        evalstring += 'obliqueProcrustesRotation_target_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        obliqueProcrustesRotation_b_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliqueProcrustesRotation_b_tmp)'
        evalstring += ','
        obliqueProcrustesRotation_t_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(obliqueProcrustesRotation_t_tmp)'
        evalstring += ','
        obliqueProcrustesRotation_factorCorrelations_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(obliqueProcrustesRotation_factorCorrelations_tmp)'
    if not (factorStructure is None):
        evalstring += ','
        evalstring += repr(IMSLS_FACTOR_STRUCTURE)
        checkForDict(factorStructure, 'factorStructure', [])
        evalstring += ','
        factorStructure_s_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(factorStructure_s_tmp)'
        evalstring += ','
        factorStructure_fvar_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(factorStructure_fvar_tmp)'
    if not (covColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_COV_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(covColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (uniqueVariancesOutput is None):
        processRet(uniqueVariancesOutput_uniqueVariancesOutput_tmp,
                   shape=(nVariables), pyvar=uniqueVariancesOutput)
    if not (eigenvalues is None):
        processRet(eigenvalues_eigenvalues_tmp,
                   shape=(nVariables), pyvar=eigenvalues)
    if not (chiSquaredTest is None):
        processRet(chiSquaredTest_df_tmp, shape=(
            1), key='df', pyvar=chiSquaredTest)
        processRet(chiSquaredTest_chiSquared_tmp, shape=(
            1), key='chiSquared', pyvar=chiSquaredTest)
        processRet(chiSquaredTest_pValue_tmp, shape=(
            1), key='pValue', pyvar=chiSquaredTest)
    if not (tuckerReliabilityCoefficient is None):
        processRet(tuckerReliabilityCoefficient_tuckerReliabilityCoefficient_tmp,
                   shape=1, pyvar=tuckerReliabilityCoefficient)
    if not (nIterations is None):
        processRet(nIterations_nIterations_tmp, shape=1, pyvar=nIterations)
    if not (functionMin is None):
        processRet(functionMin_functionMin_tmp, shape=1, pyvar=functionMin)
    if not (lastStep is None):
        processRet(lastStep_lastStep_tmp, shape=(nVariables), pyvar=lastStep)
    if not (orthomaxRotation is None):
        processRet(orthomaxRotation_b_tmp, shape=(nVariables, nFactors),
                   key='b', createArray=True, pyvar=orthomaxRotation)
        processRet(orthomaxRotation_t_tmp, shape=(nFactors, nFactors),
                   key='t', createArray=True, pyvar=orthomaxRotation)
    if not (orthogonalProcrustesRotation is None):
        processRet(orthogonalProcrustesRotation_b_tmp, shape=(
            nVariables, nFactors), key='b', createArray=True, pyvar=orthogonalProcrustesRotation)
        processRet(orthogonalProcrustesRotation_t_tmp, shape=(
            nFactors, nFactors), key='t', createArray=True, pyvar=orthogonalProcrustesRotation)
    if not (directObliminRotation is None):
        processRet(directObliminRotation_b_tmp, shape=(
            nVariables, nFactors), key='b', createArray=True, pyvar=directObliminRotation)
        processRet(directObliminRotation_t_tmp, shape=(nFactors, nFactors),
                   key='t', createArray=True, pyvar=directObliminRotation)
        processRet(directObliminRotation_factorCorrelations_tmp, shape=(
            nFactors, nFactors), key='factorCorrelations', createArray=True, pyvar=directObliminRotation)
    if not (obliquePromaxRotation is None):
        processRet(obliquePromaxRotation_target_tmp, shape=(
            nVariables, nFactors), key='target', createArray=True, pyvar=obliquePromaxRotation)
        processRet(obliquePromaxRotation_b_tmp, shape=(
            nVariables, nFactors), key='b', createArray=True, pyvar=obliquePromaxRotation)
        processRet(obliquePromaxRotation_t_tmp, shape=(nFactors, nFactors),
                   key='t', createArray=True, pyvar=obliquePromaxRotation)
        processRet(obliquePromaxRotation_factorCorrelations_tmp, shape=(
            nFactors, nFactors), key='factorCorrelation', createArray=True, pyvar=obliquePromaxRotation)
    if not (obliquePivotalPromaxRotation is None):
        processRet(obliquePivotalPromaxRotation_target_tmp, shape=(
            nVariables, nFactors), key='target', createArray=True, pyvar=obliquePivotalPromaxRotation)
        processRet(obliquePivotalPromaxRotation_b_tmp, shape=(
            nVariables, nFactors), key='b', createArray=True, pyvar=obliquePivotalPromaxRotation)
        processRet(obliquePivotalPromaxRotation_t_tmp, shape=(
            nFactors, nFactors), key='t', createArray=True, pyvar=obliquePivotalPromaxRotation)
        processRet(obliquePivotalPromaxRotation_factorCorrelations_tmp, shape=(
            nFactors, nFactors), key='factorCorrelations', createArray=True, pyvar=obliquePivotalPromaxRotation)
    if not (obliqueProcrustesRotation is None):
        processRet(obliqueProcrustesRotation_b_tmp, shape=(
            nVariables, nFactors), key='b', createArray=True, pyvar=obliqueProcrustesRotation)
        processRet(obliqueProcrustesRotation_t_tmp, shape=(
            nFactors, nFactors), key='t', createArray=True, pyvar=obliqueProcrustesRotation)
        processRet(obliqueProcrustesRotation_factorCorrelations_tmp, shape=(
            nFactors, nFactors), key='factorCorrelations', createArray=True, pyvar=obliqueProcrustesRotation)
    if not (factorStructure is None):
        processRet(factorStructure_s_tmp, shape=(nVariables, nFactors),
                   key='s', createArray=True, pyvar=factorStructure)
        processRet(factorStructure_fvar_tmp, shape=(nFactors),
                   key='fvar', createArray=True, pyvar=factorStructure)
    return processRet(result, shape=(nVariables, nFactors), result=True)
