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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, checkForList
from numpy import shape
from ctypes import POINTER, byref, c_int

imslstat = loadimsl(STAT)


def randomGfsrTableGet(table):
    imslstat.imsls_random_GFSR_table_get.restype = None
    shape = []
    evalstring = 'imslstat.imsls_random_GFSR_table_get('
    checkForList(table, 'table')
    table_tmp = POINTER(c_int)(c_int())
    evalstring += 'byref(table_tmp)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(table_tmp, shape=(1565), pyvar=table)
    return
