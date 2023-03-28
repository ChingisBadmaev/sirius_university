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
from pyimsl.stat.statStructs import Imsls_d_population
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_PRINT = 13900
imslstat = loadimsl(STAT)


def gaClonePopulation(populationIn, t_print=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ga_clone_population.restype = POINTER(Imsls_d_population)
    shape = []
    evalstring = 'imslstat.imsls_d_ga_clone_population('
    evalstring += 'populationIn'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
