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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet
from pyimsl.util.Translator import Translator
from ctypes import byref, c_int

SET_DEFAULTS = 0
SET_CENTERING = -1
GET_CENTERING = 1
SET_ROW_WRAP = -2
GET_ROW_WRAP = 2
SET_PAGING = -3
GET_PAGING = 3
SET_NAN_CHAR = -4
GET_NAN_CHAR = 4
SET_TITLE_PAGE = -5
GET_TITLE_PAGE = 5
SET_FORMAT = -6
GET_FORMAT = 6
setOptionKeywords = [SET_DEFAULTS, SET_CENTERING, SET_ROW_WRAP,
                     SET_PAGING, SET_NAN_CHAR, SET_TITLE_PAGE, SET_FORMAT]
getOptionKeywords = [GET_CENTERING, GET_ROW_WRAP,
                     GET_PAGING, GET_NAN_CHAR, GET_TITLE_PAGE, GET_FORMAT]

imslstat = loadimsl(STAT)


def writeOptions(option, optionValue):
    """ Sets or retrieves an option for printing a matrix.
    """
    imslstat.imsls_write_options.restype = None
    evalstring = 'imslstat.imsls_write_options('
    evalstring += 'c_int (option)'
    evalstring += ','
    if (option in setOptionKeywords):
        optionValue_tmp = c_int(optionValue)
    elif (option in getOptionKeywords):
        optionValue_tmp = c_int()
    else:
        errStr = Translator.getString("invalidoption")
        raise ValueError(errStr)
    evalstring += 'byref(optionValue_tmp)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if (option in getOptionKeywords):
        processRet(optionValue_tmp, inout=True, pyvar=optionValue)
    return
