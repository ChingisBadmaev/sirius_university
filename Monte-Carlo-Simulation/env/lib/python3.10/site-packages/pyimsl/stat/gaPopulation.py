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
from .statStructs import Imsls_d_population
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_PRINT = 13900
IMSLS_GRAY_ENCODING = 50711
IMSLS_FITNESS = 50724
IMSLS_FITNESS_FCN = 50725
IMSLS_FITNESS_FCN_WITH_PARMS = 50726
imslstat = loadimsl(STAT)


def gaPopulation(n, chromosome, individual, t_print=None, grayEncoding=None, fitness=None, fitnessFcn=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ga_population.restype = POINTER(Imsls_d_population)
    shape = []
    evalstring = 'imslstat.imsls_d_ga_population('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'chromosome'
    evalstring += ','
    evalstring += 'individual'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    checkForBoolean(grayEncoding, 'grayEncoding')
    if (grayEncoding):
        evalstring += ','
        evalstring += repr(IMSLS_GRAY_ENCODING)
    if not (fitness is None):
        evalstring += ','
        evalstring += repr(IMSLS_FITNESS)
        evalstring += ','
        fitness = toNumpyArray(
            fitness, 'fitness', shape=shape, dtype='double', expectedShape=(n))
        evalstring += 'fitness.ctypes.data_as(c_void_p)'
    if not (fitnessFcn is None):
        evalstring += ','
        evalstring += repr(IMSLS_FITNESS_FCN)
        evalstring += ','
        checkForCallable(fitnessFcn, 'fitnessFcn')
        TMP_FITNESSFCN_FITNESS = CFUNCTYPE(
            c_double, POINTER(Imsls_d_individual))
        tmp_fitnessFcn_fitnessFcn = TMP_FITNESSFCN_FITNESS(fitnessFcn)
        evalstring += 'tmp_fitnessFcn_fitness()'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
