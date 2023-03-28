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
from .statStructs import Imsls_d_individual
from pyimsl.util.VersionFacade import VersionFacade

IMSLS_PRINT = 13900
IMSLS_GRAY_ENCODING = 50711
IMSLS_BINARY = 50700
IMSLS_NOMINAL = 50701
IMSLS_INTEGER = 50702
IMSLS_REAL = 50703
imslstat = loadimsl(STAT)


def gaIndividual(chromosome, t_print=None, grayEncoding=None, binary=None, nominal=None, integer=None, real=None):
    VersionFacade.checkVersion(7)
    imslstat.imsls_d_ga_individual.restype = POINTER(Imsls_d_individual)
    shape = []
    evalstring = 'imslstat.imsls_d_ga_individual('
    evalstring += 'chromosome'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT)
    checkForBoolean(grayEncoding, 'grayEncoding')
    if (grayEncoding):
        evalstring += ','
        evalstring += repr(IMSLS_GRAY_ENCODING)
    if not (binary is None):
        evalstring += ','
        evalstring += repr(IMSLS_BINARY)
        evalstring += ','
        binary = toNumpyArray(binary, 'binary', shape=shape,
                              dtype='int', expectedShape=(chromosome[0].n_binary))
        evalstring += 'binary.ctypes.data_as(c_void_p)'
    if not (nominal is None):
        evalstring += ','
        evalstring += repr(IMSLS_NOMINAL)
        evalstring += ','
        nominal = toNumpyArray(nominal, 'nominal', shape=shape,
                               dtype='int', expectedShape=(chromosome[0].n_nominal))
        evalstring += 'nominal.ctypes.data_as(c_void_p)'
    if not (integer is None):
        evalstring += ','
        evalstring += repr(IMSLS_INTEGER)
        evalstring += ','
        integer = toNumpyArray(integer, 'integer', shape=shape,
                               dtype='int', expectedShape=(chromosome[0].n_integer))
        evalstring += 'integer.ctypes.data_as(c_void_p)'
    if not (real is None):
        evalstring += ','
        evalstring += repr(IMSLS_REAL)
        evalstring += ','
        real = toNumpyArray(real, 'real', shape=shape,
                            dtype='double', expectedShape=(chromosome[0].n_real))
        evalstring += 'real.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
