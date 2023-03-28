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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, processRet
from pyimsl.util.Translator import Translator
from ctypes import byref, c_int

# constants for argument 1 (option)
SET_PAGE_WIDTH = -1
GET_PAGE_WIDTH = 1
SET_PAGE_LENGTH = -2
GET_PAGE_LENGTH = 2

imslmath = loadimsl(MATH)


def page(option, pageAttribute):
    """ Sets or retrieves the page width or length.
    """
    imslmath.imsl_page.restype = None
    evalstring = 'imslmath.imsl_page('
    evalstring += 'c_int(option)'
    evalstring += ','
    if (option == SET_PAGE_WIDTH) or (option == SET_PAGE_LENGTH):
        pageAttribute_tmp = c_int(pageAttribute)
    elif (option == GET_PAGE_WIDTH) or (option == GET_PAGE_LENGTH):
        pageAttribute_tmp = c_int()
    else:
        errStr = Translator.getString("pageoptionerr")
        raise ValueError(errStr)
    evalstring += 'byref(pageAttribute_tmp)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if (option == GET_PAGE_WIDTH) or (option == GET_PAGE_LENGTH):
        processRet(pageAttribute_tmp, inout=True, pyvar=pageAttribute)
    return
