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

IMSLS_PRINT = 13900
IMSLS_GRAY_ENCODING = 50711
IMSLS_PMX_CROSSOVER = 50737
IMSLS_FITNESS_FCN = 50725
IMSLS_FITNESS_FCN_WITH_PARMS = 50726
IMSLS_BINARY_SELECTION_PROB = 50707
IMSLS_NOMINAL_SELECTION_PROB = 50708
IMSLS_INTEGER_SELECTION_MODEL = 50709
IMSLS_REAL_SELECTION_MODEL = 50710
imslstat = loadimsl(STAT)


def gaRandomPopulation(n, chromosome, t_print=None, grayEncoding=None, pmxCrossover=None, fitnessFcn=None,
                       binarySelectionProb=None, nominalSelectionProb=None, integerSelectionModel=None, realSelectionModel=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ga_random_population.restype = POINTER(Imsls_d_population)
    shape = []
    evalstring = 'imslstat.imsls_d_ga_random_population('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'chromosome'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    checkForBoolean(grayEncoding, 'grayEncoding')
    if (grayEncoding):
        evalstring += ','
        evalstring += repr(IMSLS_GRAY_ENCODING)
    checkForBoolean(pmxCrossover, 'pmxCrossover')
    if (pmxCrossover):
        evalstring += ','
        evalstring += repr(IMSLS_PMX_CROSSOVER)
    if not (fitnessFcn is None):
        evalstring += ','
        evalstring += repr(IMSLS_FITNESS_FCN)
        evalstring += ','
        checkForCallable(fitnessFcn, 'fitnessFcn')
        TMP_FITNESSFCN_FITNESSFCN = CFUNCTYPE(
            c_double, POINTER(Imsls_d_individual))
        tmp_fitnessFcn_fitnessFcn = TMP_FITNESSFCN_FITNESSFCN(fitnessFcn)
        evalstring += 'tmp_fitnessFcn_fitnessFcn'
    if not (binarySelectionProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_BINARY_SELECTION_PROB)
        evalstring += ','
        binarySelectionProb = toNumpyArray(
            binarySelectionProb, 'binarySelectionProb', shape=shape, dtype='double', expectedShape=(chromosome[0].n_binary))
        evalstring += 'binarySelectionProb.ctypes.data_as(c_void_p)'
    if not (nominalSelectionProb is None):
        evalstring += ','
        evalstring += repr(IMSLS_NOMINAL_SELECTION_PROB)
        evalstring += ','
        nominalSelectionProb = toNumpyArray(
            nominalSelectionProb, 'nominalSelectionProb', shape=shape, dtype='double', expectedShape=(chromosome[0].n_nominal))
        evalstring += 'nominalSelectionProb.ctypes.data_as(c_void_p)'
    if not (integerSelectionModel is None):
        evalstring += ','
        evalstring += repr(IMSLS_INTEGER_SELECTION_MODEL)
        checkForDict(integerSelectionModel, 'integerSelectionModel', [
                     'intSModel', 'iParms'])
        evalstring += ','
        integerSelectionModel_intSModel_tmp = integerSelectionModel['intSModel']
        integerSelectionModel_intSModel_tmp = toNumpyArray(
            intSModel, 'intSModel', shape=shape, dtype='int', expectedShape=(chromosome[0].n_integer))
        evalstring += 'integerSelectionModel_intSModel_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        integerSelectionModel_iParms_tmp = integerSelectionModel['iParms']
        integerSelectionModel_iParms_tmp = toNumpyArray(
            iParms, 'iParms', shape=shape, dtype='double', expectedShape=(2, chromosome[0].n_integer))
        evalstring += 'integerSelectionModel_iParms_tmp.ctypes.data_as(c_void_p)'
    if not (realSelectionModel is None):
        evalstring += ','
        evalstring += repr(IMSLS_REAL_SELECTION_MODEL)
        checkForDict(realSelectionModel, 'realSelectionModel',
                     ['realSModel', 'rParms'])
        evalstring += ','
        realSelectionModel_realSModel_tmp = realSelectionModel['realSModel']
        realSelectionModel_realSModel_tmp = toNumpyArray(
            realSModel, 'realSModel', shape=shape, dtype='int', expectedShape=(chromosome[0].n_real))
        evalstring += 'realSelectionModel_realSModel_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        realSelectionModel_rParms_tmp = realSelectionModel['rParms']
        realSelectionModel_rParms_tmp = toNumpyArray(
            rParms, 'rParms', shape=shape, dtype='double', expectedShape=(2, chromosome.n_real))
        evalstring += 'realSelectionModel_rParms_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (integerSelectionModel is None):
        processRet(integerSelectionModel_intSModel_tmp, shape=(
            chromosome[0].n_integer), key='intSModel', inout=True, pyvar=integerSelectionModel)
        processRet(integerSelectionModel_iParms_tmp, shape=(
            2, chromosome[0].n_integer), key='iParms', inout=True, pyvar=integerSelectionModel)
    if not (realSelectionModel is None):
        processRet(realSelectionModel_realSModel_tmp, shape=(
            chromosome[0].n_real), key='realSModel', inout=True, pyvar=realSelectionModel)
        processRet(realSelectionModel_rParms_tmp, shape=(
            2, chromosome[0].n_real), key='rParms', inout=True, pyvar=realSelectionModel)
    return result
