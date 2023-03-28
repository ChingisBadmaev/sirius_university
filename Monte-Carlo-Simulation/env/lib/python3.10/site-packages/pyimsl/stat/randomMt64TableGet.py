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
from pyimsl.util.VersionFacade import VersionFacade
imslstat = loadimsl(STAT)


def randomMt64TableGet(table):
    VersionFacade.checkVersion(6)
    imslstat.imsls_random_MT64_table_get.restype = None
    shape = []
    checkForList(table, 'table')
    evalstring = 'imslstat.imsls_random_MT64_table_get('
    table_tmp = POINTER(c_ulonglong)(c_ulonglong())
    evalstring += 'byref(table_tmp)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    # Special handling for unsigned long long output var.
    # To use an ndarray as output you must declare it as
    # empty(0,dtype='ulonglong')
    if isinstance(table, ndarray):
        table.resize(625, dtype='ulonglong', refcheck=0)
        for i in range(0, 625):
            table[i] = table_tmp[i]
    else:
        table[:] = []
        for i in range(0, 625):
            table.append(table_tmp[i])
    return
