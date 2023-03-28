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
from numpy import ndim, shape
from ctypes import POINTER, c_int
from .statStructs import Imsls_faure

IMSLS_BASE = 40016
IMSLS_SKIP = 40017
imslstat = loadimsl(STAT)


def faureSequenceInit(ndim, base=None, skip=None):
    imslstat.imsls_faure_sequence_init.restype = POINTER(Imsls_faure)
    shape = []
    evalstring = 'imslstat.imsls_faure_sequence_init('
    evalstring += 'c_int(ndim)'
    if not (base is None):
        evalstring += ','
        evalstring += repr(IMSLS_BASE)
        evalstring += ','
        evalstring += 'c_int(base)'
    if not (skip is None):
        evalstring += ','
        evalstring += repr(IMSLS_SKIP)
        evalstring += ','
        evalstring += 'c_int(skip)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
