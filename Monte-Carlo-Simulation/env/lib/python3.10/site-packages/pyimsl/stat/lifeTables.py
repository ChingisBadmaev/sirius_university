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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_PRINT_LEVEL = 20530
IMSLS_POPULATION_SIZE = 40042
IMSLS_POPULATION_LIFE_TABLE = 40043
imslstat = loadimsl(STAT)


def lifeTables(age, a, nCohort, printLevel=None, populationSize=None, populationLifeTable=None):
    """ Produces population and cohort life tables.
    """
    imslstat.imsls_d_life_tables.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_life_tables('
    evalstring += 'c_int(nClasses)'
    evalstring += ','
    age = toNumpyArray(age, 'age', shape=shape,
                       dtype='double', expectedShape=(0))
    evalstring += 'age.ctypes.data_as(c_void_p)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    nClasses = shape[0]
    evalstring += ','
    nCohort = toNumpyArray(nCohort, 'nCohort', shape=shape,
                           dtype='int', expectedShape=(nClasses))
    evalstring += 'nCohort.ctypes.data_as(c_void_p)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (populationSize is None):
        evalstring += ','
        evalstring += repr(IMSLS_POPULATION_SIZE)
        evalstring += ','
        evalstring += 'c_int(populationSize)'
    if not (populationLifeTable is None):
        evalstring += ','
        evalstring += repr(IMSLS_POPULATION_LIFE_TABLE)
        evalstring += ','
        evalstring += 'c_int(populationLifeTable)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nClasses, 12), result=True)
