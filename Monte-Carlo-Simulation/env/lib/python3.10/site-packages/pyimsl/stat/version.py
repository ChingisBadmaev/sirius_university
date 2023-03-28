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
from pyimsl.util.Translator import Translator
from numpy import shape
from ctypes import c_char_p, c_int

# Legal values for "code":
LIBRARY_VERSION = 12760
OS_VERSION = 13630
COMPILER_VERSION = 10780
LICENSE_NUMBER = 12770

imslstat = loadimsl(STAT)


def version(code):
    """ Returns information describing the version of the library, serial number, operating system, and compiler.
    """
    if (code != OS_VERSION) and (code != COMPILER_VERSION) and (code != LIBRARY_VERSION) and (code != LICENSE_NUMBER):
        errStr = Translator.getString("invalidcode")
        raise ValueError(errStr)

    imslstat.imsls_version.restype = c_char_p
    shape = []
    evalstring = 'imslstat.imsls_version('
    evalstring += 'c_int(code)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return bytes.decode(result)
