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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl
from pyimsl.util.VersionFacade import VersionFacade
from pyimsl.util.Translator import Translator
from numpy import shape
from ctypes import c_int

imslstat = loadimsl(STAT)


def randomOption(generatorOption):
    """ Selects the uniform (0,1) multiplicative congruential pseudorandom number generator or a generalized feedback shift register (GFSR) method.
    """
    imslstat.imsls_random_option.restype = None
    ver = VersionFacade.getCnlVersion()
    if ver.majorVersion == 5:
        if generatorOption > 7:
            errStr = Translator.getString("randomOptionErr")
            raise ValueError(errStr)
    else:
        if generatorOption > 9:
            errStr = Translator.getString("randomOptionErr2")
            raise ValueError(errStr)
    evalstring = 'imslstat.imsls_random_option('
    evalstring += 'c_int(generatorOption)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
