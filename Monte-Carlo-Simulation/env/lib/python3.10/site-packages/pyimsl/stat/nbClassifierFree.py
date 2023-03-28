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
from pyimsl.util.VersionFacade import VersionFacade
from numpy import array, empty
from ctypes import *

imslstat = loadimsl(STAT)


def nbClassifierFree(nbClassifier):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_nb_classifier_free.restype = None
    evalstring = 'imslstat.imsls_d_nb_classifier_free('
    evalstring += 'nbClassifier[0].state'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
