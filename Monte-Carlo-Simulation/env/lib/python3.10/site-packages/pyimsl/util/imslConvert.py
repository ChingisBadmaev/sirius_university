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
from numpy import ndarray, empty, double, flatiter

# Utility routines for data conversion. Primarilly for arrays in user functions

# Return numpy from ctype array


def toNdarray(ctype, shape, dtype=double):
    if (isinstance(ctype, ndarray)
            or isinstance(ctype, list)
            or isinstance(ctype, tuple)):  # already a numpy/list/tuple
        return ctype
    else:
        pyvar = empty(shape, dtype=dtype)
        flatiter = pyvar.flat
        flatiter[:] = ctype[0:len(flatiter)]
        return pyvar
    # TODO: handle dtypes for complex
    # (but complex can't be currently used in user functions so may not be needed)

# Replace values in ctypy array from numpy


def toCtypes(numpy, ctype):
    # TODO: handle complex
    flatiter = numpy.flat
    for i in range(len(flatiter)):
        ctype[i] = flatiter[i]
