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
from .statStructs import Imsls_d_svm_model

IMSLS_SVM_C_SVC_TYPE = 50957
IMSLS_SVM_NU_SVC_TYPE = 50958
IMSLS_SVM_ONE_CLASS_TYPE = 50959
IMSLS_SVM_EPSILON_SVR_TYPE = 50960
IMSLS_SVM_NU_SVR_TYPE = 50961
IMSLS_SVM_WORK_ARRAY_SIZE = 50967
IMSLS_SVM_EPSILON = 50968
IMSLS_SVM_NO_SHRINKING = 50969
IMSLS_SVM_TRAIN_ESTIMATE_PROB = 50971
IMSLS_SVM_KERNEL_LINEAR = 50962
IMSLS_SVM_KERNEL_POLYNOMIAL = 50963
IMSLS_SVM_KERNEL_RADIAL_BASIS = 50964
IMSLS_SVM_KERNEL_SIGMOID = 50965
IMSLS_SVM_KERNEL_PRECOMPUTED = 50966
IMSLS_SVM_CROSS_VALIDATION = 50970
imslstat = loadimsl(STAT)


def supportVectorTrainer(nClasses, classification, x, svmCSvcType=None, svmNuSvcType=None, svmOneClassType=None, svmEpsilonSvrType=None, svmNuSvrType=None, svmWorkArraySize=None, svmNoShrinking=None, svmTrainEstimateProb=None, svmKernelLinear=None, svmKernelPolynomial=None, svmKernelRadialBasis=None, svmKernelSigmoid=None, svmKernelPrecomputed=None, svmCrossValidation=None, svmEpsilon=None):
    """ Trains a Support Vector Machines (SVM) classifier.
    """
    # imslstat.imsls_d_support_vector_trainer.restype = struct
    imslstat.imsls_d_support_vector_trainer.restype = POINTER(
        Imsls_d_svm_model)
    shape = []
    evalstring = 'imslstat.imsls_d_support_vector_trainer('
    evalstring += 'c_int(nPatterns)'
    evalstring += ','
    evalstring += 'c_int(nClasses)'
    evalstring += ','
    evalstring += 'c_int(nAttributes)'
    evalstring += ','
    classification = toNumpyArray(
        classification, 'classification', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'classification.ctypes.data_as(c_void_p)'
    nPatterns = shape[0]
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                     expectedShape=(nPatterns, 0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nAttributes = shape[1]
    if not (svmCSvcType is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_C_SVC_TYPE)
        checkForDict(svmCSvcType, 'svmCSvcType', [
                     'C', 'weightClass', 'weight'])
        evalstring += ','
        svmCSvcType_c_tmp = svmCSvcType['C']
        evalstring += 'c_double(svmCSvcType_c_tmp)'
        evalstring += ','
        evalstring += 'c_int(svmCSvcType_nrWeight_tmp)'
        evalstring += ','
        svmCSvcType_weightClass_tmp = svmCSvcType['weightClass']
        svmCSvcType_weightClass_tmp = toNumpyArray(
            svmCSvcType_weightClass_tmp, 'weightClass', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'svmCSvcType_weightClass_tmp.ctypes.data_as(c_void_p)'
        svmCSvcType_nrWeight_tmp = shape[0]
        evalstring += ','
        svmCSvcType_weight_tmp = svmCSvcType['weight']
        svmCSvcType_weight_tmp = toNumpyArray(
            svmCSvcType_weight_tmp, 'weight', shape=shape, dtype='double', expectedShape=(svmCSvcType_nrWeight_tmp))
        evalstring += 'svmCSvcType_weight_tmp.ctypes.data_as(c_void_p)'
    if not (svmNuSvcType is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_NU_SVC_TYPE)
        evalstring += ','
        evalstring += 'c_double(svmNuSvcType)'
    if not (svmOneClassType is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_ONE_CLASS_TYPE)
        evalstring += ','
        evalstring += 'c_double(svmOneClassType)'
    if not (svmEpsilonSvrType is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_EPSILON_SVR_TYPE)
        checkForDict(svmEpsilonSvrType, 'svmEpsilonSvrType', ['C', 'p'])
        evalstring += ','
        svmEpsilonSvrType_c_tmp = svmEpsilonSvrType['C']
        evalstring += 'c_double(svmEpsilonSvrType_c_tmp)'
        evalstring += ','
        svmEpsilonSvrType_p_tmp = svmEpsilonSvrType['p']
        evalstring += 'c_double(svmEpsilonSvrType_p_tmp)'
    if not (svmNuSvrType is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_NU_SVR_TYPE)
        checkForDict(svmNuSvrType, 'svmNuSvrType', ['C', 'nu'])
        evalstring += ','
        svmNuSvrType_c_tmp = svmNuSvrType['C']
        evalstring += 'c_double(svmNuSvrType_c_tmp)'
        evalstring += ','
        svmNuSvrType_nu_tmp = svmNuSvrType['nu']
        evalstring += 'c_double(svmNuSvrType_nu_tmp)'
    if not (svmWorkArraySize is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_WORK_ARRAY_SIZE)
        evalstring += ','
        evalstring += 'c_double(svmWorkArraySize)'
    checkForBoolean(svmNoShrinking, 'svmNoShrinking')
    if (svmNoShrinking):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_NO_SHRINKING)
    checkForBoolean(svmTrainEstimateProb, 'svmTrainEstimateProb')
    if (svmTrainEstimateProb):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_TRAIN_ESTIMATE_PROB)
    checkForBoolean(svmKernelLinear, 'svmKernelLinear')
    if (svmKernelLinear):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_KERNEL_LINEAR)
    if not (svmKernelPolynomial is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_KERNEL_POLYNOMIAL)
        checkForDict(svmKernelPolynomial, 'svmKernelPolynomial',
                     ['degree', 'gamma', 'coef0'])
        evalstring += ','
        svmKernelPolynomial_degree_tmp = svmKernelPolynomial['degree']
        evalstring += 'c_int(svmKernelPolynomial_degree_tmp)'
        evalstring += ','
        svmKernelPolynomial_gamma_tmp = svmKernelPolynomial['gamma']
        evalstring += 'c_double(svmKernelPolynomial_gamma_tmp)'
        evalstring += ','
        svmKernelPolynomial_coef0_tmp = svmKernelPolynomial['coef0']
        evalstring += 'c_double(svmKernelPolynomial_coef0_tmp)'
    if not (svmKernelRadialBasis is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_KERNEL_RADIAL_BASIS)
        evalstring += ','
        evalstring += 'c_double(svmKernelRadialBasis)'
    if not (svmEpsilon is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_EPSILON)
        evalstring += ','
        evalstring += 'c_double(svmEpsilon)'
    if not (svmKernelSigmoid is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_KERNEL_SIGMOID)
        checkForDict(svmKernelSigmoid, 'svmKernelSigmoid', ['gamma', 'coef0'])
        evalstring += ','
        svmKernelSigmoid_gamma_tmp = svmKernelSigmoid['gamma']
        evalstring += 'c_double(svmKernelSigmoid_gamma_tmp)'
        evalstring += ','
        svmKernelSigmoid_coef0_tmp = svmKernelSigmoid['coef0']
        evalstring += 'c_double(svmKernelSigmoid_coef0_tmp)'
    if not (svmKernelPrecomputed is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_KERNEL_PRECOMPUTED)
        evalstring += ','
        svmKernelPrecomputed = toNumpyArray(
            svmKernelPrecomputed, 'svmKernelPrecomputed', shape=shape, dtype='double', expectedShape=(nPatterns, nPatterns))
        evalstring += 'svmKernelPrecomputed.ctypes.data_as(c_void_p)'
    if not (svmCrossValidation is None):
        evalstring += ','
        evalstring += repr(IMSLS_SVM_CROSS_VALIDATION)
        checkForDict(svmCrossValidation, 'svmCrossValidation', ['nFolds'])
        evalstring += ','
        svmCrossValidation_nFolds_tmp = svmCrossValidation['nFolds']
        evalstring += 'c_int(svmCrossValidation_nFolds_tmp)'
        evalstring += ','
        svmCrossValidation_target_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(svmCrossValidation_target_tmp)'
        evalstring += ','
        svmCrossValidation_result_tmp = c_double()
        evalstring += 'byref(svmCrossValidation_result_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (svmCrossValidation is None):
        processRet(svmCrossValidation_target_tmp, shape=(
            nPatterns), key='target', pyvar=svmCrossValidation)
        processRet(svmCrossValidation_result_tmp, shape=(
            1), key='result', pyvar=svmCrossValidation)
    # return processRet (result, shape=(1), result=True)
    return result
