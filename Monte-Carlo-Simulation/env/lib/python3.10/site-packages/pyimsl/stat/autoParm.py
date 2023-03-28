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

IMSLS_MAX_AR_ORDER = 50897
IMSLS_METHOD = 13170
IMSLS_MODEL_SELECTION_CRITERION = 50632
IMSLS_MAXIMUM_LIKELIHOOD = 12900
IMSLS_AR_MODEL = 50896
IMSLS_PRINT = 13900
IMSLS_RANDOM_SEED = 50600
IMSLS_PROB_DISTRIBUTION = 50895
IMSLS_MIN_OBSERVATIONS = 50886
IMSLS_GA_PARAMETERS = 50887
IMSLS_ISLAND = 50888
IMSLS_MAX_MIGRATIONS = 50889
IMSLS_STOP_ITERATIONS = 50890
IMSLS_SELECTION_CRITERION_VALUE = 50898
IMSLS_AR_FIT = 50891
IMSLS_AR_STATS = 50893
imslstat = loadimsl(STAT)


def autoParm(y, npcs, maxArOrder=None, method=None, modelSelectionCriterion=None, maximumLikelihood=None, arModel=None, t_print=None, randomSeed=None, probDistribution=None, minObservations=None, gaParameters=None, island=None, maxMigrations=None, stopIterations=None, selectionCriterionValue=None, arFit=None, arStats=None):
    imslstat.imsls_d_auto_parm.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_d_auto_parm('
    evalstring += 'c_int(nobs)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    nobs = shape[0]
    evalstring += ','
    npcs_tmp = npcs
    if (not(isinstance(npcs_tmp, c_int))):
        npcs_tmp = c_int(npcs[0])
    evalstring += 'byref(npcs_tmp)'
    if not (maxArOrder is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_AR_ORDER)
        evalstring += ','
        evalstring += 'c_int(maxArOrder)'
    else:
        maxArOrder = 20
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (modelSelectionCriterion is None):
        evalstring += ','
        evalstring += repr(IMSLS_MODEL_SELECTION_CRITERION)
        evalstring += ','
        evalstring += 'c_int(modelSelectionCriterion)'
    if not (maximumLikelihood is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAXIMUM_LIKELIHOOD)
        evalstring += ','
        evalstring += 'c_int(maximumLikelihood)'
    if not (arModel is None):
        evalstring += ','
        evalstring += repr(IMSLS_AR_MODEL)
        evalstring += ','
        arModel = toNumpyArray(
            arModel, 'arModel', shape=shape, dtype='int', expectedShape=(npcs[0], 2))
        evalstring += 'arModel.ctypes.data_as(c_void_p)'
    if not (t_print is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
        evalstring += ','
        evalstring += 'c_int(t_print)'
    if not (randomSeed is None):
        evalstring += ','
        evalstring += repr(IMSLS_RANDOM_SEED)
        evalstring += ','
        evalstring += 'c_int(randomSeed)'
    if not (probDistribution is None):
        evalstring += ','
        evalstring += repr(IMSLS_PROB_DISTRIBUTION)
        evalstring += ','
        probDistribution = toNumpyArray(
            probDistribution, 'probDistribution', shape=shape, dtype='double', expectedShape=(maxArOrder + 1))
        evalstring += 'probDistribution.ctypes.data_as(c_void_p)'
    if not (minObservations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MIN_OBSERVATIONS)
        evalstring += ','
        minObservations = toNumpyArray(
            minObservations, 'minObservations', shape=shape, dtype='int', expectedShape=(maxArOrder + 1))
        evalstring += 'minObservations.ctypes.data_as(c_void_p)'
    if not (gaParameters is None):
        evalstring += ','
        evalstring += repr(IMSLS_GA_PARAMETERS)
        evalstring += ','
        gaParameters = toNumpyArray(
            gaParameters, 'gaParameters', shape=shape, dtype='double', expectedShape=(4))
        evalstring += 'gaParameters.ctypes.data_as(c_void_p)'
    if not (island is None):
        evalstring += ','
        evalstring += repr(IMSLS_ISLAND)
        evalstring += ','
        island = toNumpyArray(island, 'island', shape=shape,
                              dtype='int', expectedShape=(5))
        evalstring += 'island.ctypes.data_as(c_void_p)'
    if not (maxMigrations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_MIGRATIONS)
        evalstring += ','
        evalstring += 'c_int(maxMigrations)'
    if not (stopIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_STOP_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(stopIterations)'
    if not (selectionCriterionValue is None):
        evalstring += ','
        evalstring += repr(IMSLS_SELECTION_CRITERION_VALUE)
        checkForList(selectionCriterionValue, 'selectionCriterionValue')
        evalstring += ','
        selectionCriterionValue_value_tmp = c_double()
        evalstring += 'byref(selectionCriterionValue_value_tmp)'
    if not (arFit is None):
        evalstring += ','
        evalstring += repr(IMSLS_AR_FIT)
        checkForList(arFit, 'arFit')
        evalstring += ','
        arFit_arfit_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(arFit_arfit_tmp)'
    if not (arStats is None):
        evalstring += ','
        evalstring += repr(IMSLS_AR_STATS)
        checkForList(arStats, 'arStats')
        evalstring += ','
        arStats_arstat_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(arStats_arstat_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(npcs_tmp, inout=True, shape=(1), pyvar=npcs)
    if not (selectionCriterionValue is None):
        processRet(selectionCriterionValue_value_tmp,
                   shape=(1), pyvar=selectionCriterionValue)
    if not (arFit is None):
        processRet(arFit_arfit_tmp, shape=(npcs_tmp, maxArOrder), pyvar=arFit)
    if not (arStats is None):
        processRet(arStats_arstat_tmp, shape=(npcs_tmp, 2), pyvar=arStats)
    return processRet(result, shape=(npcs_tmp, 2), result=True)
