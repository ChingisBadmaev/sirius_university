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
from numpy import shape
from ctypes import c_int, c_ulonglong

imslstat = loadimsl(STAT)


def randomMt64Init(key):
    VersionFacade.checkVersion(6)
    imslstat.imsls_random_MT64_init.restype = None
    shape = []
    evalstring = 'imslstat.imsls_random_MT64_init('
    evalstring += 'c_int(keyLength)'
    evalstring += ','
#
# Convert key to c_ulonglong, for later use
#
    key_type = c_ulonglong * len(key)
    key_tmp = key_type()
    for i in range(0, len(key)):
        key_tmp[i] = key[i]
    evalstring += 'key_tmp'
    keyLength = len(key)
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return
