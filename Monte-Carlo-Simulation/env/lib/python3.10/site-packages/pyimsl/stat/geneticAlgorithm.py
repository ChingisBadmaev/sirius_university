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
from pyimsl.stat.statStructs import Imsls_d_individual
from pyimsl.stat.statStructs import Imsls_d_population
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_GRAY_ENCODING = 50711
IMSLS_NO_ELITISM = 50716
IMSLS_NO_DECODE = 50736
IMSLS_PRINT_LEVEL = 20530
IMSLS_MAX_GENERATIONS = 50717
IMSLS_MAX_FITNESS = 50731
IMSLS_LINEAR_SCALING = 50718
IMSLS_SIGMA_SCALING = 50719
IMSLS_GENERATION_GAP = 50729
IMSLS_MUTATION_PROB = 50720
IMSLS_CROSSOVER_PROB = 50721
IMSLS_CROSSOVERS = 50722
IMSLS_PMX_CROSSOVER = 50737
IMSLS_INVERT_CROSSOVER = 50738
IMSLS_SELECTION_MODEL = 50723
IMSLS_FITNESS_FCN_WITH_PARMS = 50726
IMSLS_N_GENERATIONS = 50730
IMSLS_ON_LINE_PERFORMANCE = 50733
IMSLS_OFF_LINE_PERFORMANCE = 50734
IMSLS_VELOCITY = 50732
IMSLS_GENERATION_STATS = 50727
IMSLS_LAST_GENERATION = 50728

# Print levels for printLevel keyword
NONE = 0
FINAL = 1
TRACE_GEN = 2
TRACE_ALL = 3

# Selection Model
ROULETTE_WITH = 0
ROULETTE_WITHOUT = 1
DETERMINISTIC = 2
REMAINDER_WITH = 3
REMAINDER_WITHOUT = 4
SUS_SELECTION = 5
RANK_SELECTION = 6
TOURNAMENT_1 = 7
TOURNAMENT_2 = 8

imslstat = loadimsl(STAT)


def geneticAlgorithm(fitness, initialPopulation, grayEncoding=None, noElitism=None, noDecode=None,
                     printLevel=None, maxGenerations=None, maxFitness=None, linearScaling=None, sigmaScaling=None,
                     generationGap=None, mutationProb=None, crossoverProb=None, crossovers=None, pmxCrossover=None,
                     invertCrossover=None, selectionModel=None, nGenerations=None, onLinePerformance=None,
                     offLinePerformance=None, velocity=None, generationStats=None, lastGeneration=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_genetic_algorithm.restype = POINTER(Imsls_d_individual)
    shape = []
    evalstring = 'imslstat.imsls_d_genetic_algorithm('
    checkForCallable(fitness, 'fitness')
    TMP_FITNESS = CFUNCTYPE(c_double, POINTER(Imsls_d_individual))
    tmp_fitness = TMP_FITNESS(fitness)
    evalstring += 'tmp_fitness'
    evalstring += ','
    evalstring += 'initialPopulation'
    checkForBoolean(grayEncoding, 'grayEncoding')
    if (grayEncoding):
        evalstring += ','
        evalstring += repr(IMSLS_GRAY_ENCODING)
    checkForBoolean(noElitism, 'noElitism')
    if (noElitism):
        evalstring += ','
        evalstring += repr(IMSLS_NO_ELITISM)
    checkForBoolean(noDecode, 'noDecode')
    if (noDecode):
        evalstring += ','
        evalstring += repr(IMSLS_NO_DECODE)
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (maxGenerations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_GENERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxGenerations)'
    if not (maxFitness is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_FITNESS)
        evalstring += ','
        evalstring += 'c_double(maxFitness)'
    if not (linearScaling is None):
        evalstring += ','
        evalstring += repr(IMSLS_LINEAR_SCALING)
        evalstring += ','
        evalstring += 'c_double(linearScaling)'
    checkForBoolean(sigmaScaling, 'sigmaScaling')
    if (sigmaScaling):
        evalstring += ','
        evalstring += repr(IMSLS_SIGMA_SCALING)
    if not (generationGap is None):
        evalstring += ','
        evalstring += repr(IMSLS_GENERATION_GAP)
        evalstring += ','
        evalstring += 'c_double(generationGap)'
    if not (mutationProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_MUTATION_PROB)
        evalstring += ','
        evalstring += 'c_double(mutationProb)'
    if not (crossoverProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_CROSSOVER_PROB)
        evalstring += ','
        evalstring += 'c_double(crossoverProb)'
    if not (crossovers is None):
        evalstring += ','
        evalstring += repr(IMSLS_CROSSOVERS)
        evalstring += ','
        evalstring += 'c_int(crossovers)'
    checkForBoolean(pmxCrossover, 'pmxCrossover')
    if (pmxCrossover):
        evalstring += ','
        evalstring += repr(IMSLS_PMX_CROSSOVER)
    checkForBoolean(invertCrossover, 'invertCrossover')
    if (invertCrossover):
        evalstring += ','
        evalstring += repr(IMSLS_INVERT_CROSSOVER)
    if not (selectionModel is None):
        evalstring += ','
        evalstring += repr(IMSLS_SELECTION_MODEL)
        evalstring += ','
        evalstring += 'c_int(selectionModel)'
    if not (nGenerations is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_GENERATIONS)
        checkForList(nGenerations, 'nGenerations')
        evalstring += ','
        nGenerations_nGenerations_tmp = c_int()
        evalstring += 'byref(nGenerations_nGenerations_tmp)'
    if not (onLinePerformance is None):
        evalstring += ','
        evalstring += repr(IMSLS_ON_LINE_PERFORMANCE)
        checkForList(onLinePerformance, 'onLinePerformance')
        evalstring += ','
        onLinePerformance_onLinePerformance_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(onLinePerformance_onLinePerformance_tmp)'
    if not (offLinePerformance is None):
        evalstring += ','
        evalstring += repr(IMSLS_OFF_LINE_PERFORMANCE)
        checkForList(offLinePerformance, 'offLinePerformance')
        evalstring += ','
        offLinePerformance_offLinePerformance_tmp = POINTER(
            c_double)(c_double())
        evalstring += 'byref(offLinePerformance_offLinePerformance_tmp)'
    if not (velocity is None):
        evalstring += ','
        evalstring += repr(IMSLS_VELOCITY)
        checkForList(velocity, 'velocity')
        evalstring += ','
        velocity_velocity_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(velocity_velocity_tmp)'
    if not (generationStats is None):
        evalstring += ','
        evalstring += repr(IMSLS_GENERATION_STATS)
        checkForList(generationStats, 'generationStats')
        evalstring += ','
        generationStats_genStatistics_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(generationStats_genStatistics_tmp)'
    if not (lastGeneration is None):
        evalstring += ','
        evalstring += repr(IMSLS_LAST_GENERATION)
        checkForList(lastGeneration, 'lastGeneration')
        evalstring += ','
        lastGeneration_lastGeneration_tmp = POINTER(
            Imsls_d_population)(Imsls_d_population())
        evalstring += 'byref(lastGeneration_lastGeneration_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nGenerations is None):
        processRet(nGenerations_nGenerations_tmp,
                   shape=(1), pyvar=nGenerations)
    if not (onLinePerformance is None):
        processRet(onLinePerformance_onLinePerformance_tmp,
                   shape=(maxGenerations), pyvar=onLinePerformance)
    if not (offLinePerformance is None):
        processRet(offLinePerformance_offLinePerformance_tmp,
                   shape=(maxGenerations), pyvar=offLinePerformance)
    if not (velocity is None):
        processRet(velocity_velocity_tmp, shape=(
            maxGenerations), pyvar=velocity)
    if not (generationStats is None):
        processRet(generationStats_genStatistics_tmp, shape=(
            maxGenerations + 1, 4), pyvar=generationStats)
    if not (lastGeneration is None):
        lastGeneration[:] = []
        lastGeneration.append(lastGeneration_lastGeneration_tmp)
    return result
