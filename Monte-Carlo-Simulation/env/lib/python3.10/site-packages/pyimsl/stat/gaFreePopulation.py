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

imslstat = loadimsl(STAT)


def gaFreePopulation(population):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ga_free_population.restype = None
    imslstat.imsls_d_ga_free_population.arglist = [POINTER(Imsls_d_population)]
    shape = []
    evalstring = 'imslstat.imsls_d_ga_free_population('
    evalstring += 'population'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
