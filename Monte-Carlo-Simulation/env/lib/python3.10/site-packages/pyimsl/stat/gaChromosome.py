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
from .statStructs import Imsls_d_chromosome
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_PRINT = 13900
IMSLS_BINARY = 50700
IMSLS_NOMINAL = 50701
IMSLS_INTEGER = 50702
IMSLS_REAL = 50703
imslstat = loadimsl(STAT)


def gaChromosome(t_print=None, binary=None, nominal=None, integer=None, real=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ga_chromosome.restype = POINTER(Imsls_d_chromosome)
    shape = []
    first = True
    evalstring = 'imslstat.imsls_d_ga_chromosome('
    checkForBoolean(t_print, 't_print')
    if (t_print):
        if (first):
            first = False
        else:
            evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    if not (binary is None):
        if (first):
            first = False
        else:
            evalstring += ','
        evalstring += repr(IMSLS_BINARY)
        evalstring += ','
        evalstring += 'c_int(binary)'
    if not (nominal is None):
        if (first):
            first = False
        else:
            evalstring += ','
        evalstring += repr(IMSLS_NOMINAL)
        evalstring += ','
        evalstring += 'c_int(nominal_nNominal_tmp)'
        evalstring += ','
        nominal_nCategories_tmp = toNumpyArray(
            nominal, 'nominal', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'nominal_nCategories_tmp.ctypes.data_as(c_void_p)'
        nominal_nNominal_tmp = shape[0]
    if not (integer is None):
        if (first):
            first = False
        else:
            evalstring += ','
        evalstring += repr(IMSLS_INTEGER)
        checkForDict(integer, 'integer', ['iIntervals', 'iBounds'])
        evalstring += ','
        evalstring += 'c_int(integer_nInteger_tmp)'
        evalstring += ','
        integer_iIntervals_tmp = integer['iIntervals']
        integer_iIntervals_tmp = toNumpyArray(
            integer_iIntervals_tmp, 'iIntervals', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'integer_iIntervals_tmp.ctypes.data_as(c_void_p)'
        integer_nInteger_tmp = shape[0]
        evalstring += ','
        integer_iBounds_tmp = integer['iBounds']
        integer_iBounds_tmp = toNumpyArray(
            integer_iBounds_tmp, 'iBounds', shape=shape, dtype='int', expectedShape=(integer_nInteger_tmp, 2))
        evalstring += 'integer_iBounds_tmp.ctypes.data_as(c_void_p)'
    if not (real is None):
        if (first):
            first = False
        else:
            evalstring += ','
        evalstring += repr(IMSLS_REAL)
        checkForDict(real, 'real', ['rIntervals', 'rBounds'])
        evalstring += ','
        evalstring += 'c_int(real_nReal_tmp)'
        evalstring += ','
        real_rIntervals_tmp = real['rIntervals']
        real_rIntervals_tmp = toNumpyArray(
            real_rIntervals_tmp, 'rIntervals', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'real_rIntervals_tmp.ctypes.data_as(c_void_p)'
        real_nReal_tmp = shape[0]
        evalstring += ','
        real_rBounds_tmp = real['rBounds']
        real_rBounds_tmp = toNumpyArray(
            real_rBounds_tmp, 'rBounds', shape=shape, dtype='double', expectedShape=(real_nReal_tmp, 2))
        evalstring += 'real_rBounds_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
