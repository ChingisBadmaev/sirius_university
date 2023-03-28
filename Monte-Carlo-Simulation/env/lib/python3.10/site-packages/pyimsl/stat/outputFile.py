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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl
from pyimsl.util.Translator import Translator
from numpy import shape
from ctypes import byref, c_long
from ctypes import c_void_p

IMSLS_SET_OUTPUT_FILE = 14510
IMSLS_GET_OUTPUT_FILE = 11980
IMSLS_SET_ERROR_FILE = 14490
IMSLS_GET_ERROR_FILE = 11970
imslstat = loadimsl(STAT)


def outputFile(setOutputFile=None, getOutputFile=None, setErrorFile=None, getErrorFile=None):
    imslstat.imsls_output_file.restype = None
    shape = []
    evalstring = 'imslstat.imsls_output_file('
    if not (setOutputFile is None):
        evalstring += repr(IMSLS_SET_OUTPUT_FILE)
        evalstring += ','
        # evalstring +='setOutputFile'
        evalstring += 'c_void_p(setOutputFile)'
    if not (getOutputFile is None):
        if(evalstring.count(',') > 0):
            evalstring += ','
        evalstring += repr(IMSLS_GET_OUTPUT_FILE)
        checkForList(getOutputFile, 'getOutputFile')
        evalstring += ','
        getOutputFile_pofile_tmp = c_void_p()
        evalstring += 'byref(getOutputFile_pofile_tmp)'
    if not (setErrorFile is None):
        if(evalstring.count(',') > 0):
            evalstring += ','
        evalstring += repr(IMSLS_SET_ERROR_FILE)
        evalstring += ','
        evalstring += 'struct(setErrorFile)'
    if not (getErrorFile is None):
        if(evalstring.count(',') > 0):
            evalstring += ','
        evalstring += repr(IMSLS_GET_ERROR_FILE)
        checkForList(getErrorFile, 'getErrorFile')
        evalstring += ','
        getErrorFile_pefile_tmp = c_void_p()
        evalstring += 'byref(getErrorFile_pefile_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)

    if not (getOutputFile is None):
        getOutputFile[:] = []
        getOutputFile.append(getOutputFile_pofile_tmp.value)
    if not (getErrorFile is None):
        getErrorFile[:] = []
        getErrorFile.append(getErrorFile_pefile_tmp.value)
    return
