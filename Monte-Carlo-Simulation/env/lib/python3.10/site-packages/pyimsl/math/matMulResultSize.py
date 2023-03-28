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


def matMulCountMatrices(operation):
    # Calculate the number of times A, B, X, and Y occur in
    # the expression.

    # The expression string, which is delimited by asterisks,
    # can contain any of the following substrings:

    #   A, B, x, y
    #   trans(A), trans(B), trans(x), trans(y)
    #   ctrans(A), ctrans(B), ctrans(x), ctrans(y)
    # Return value: a list, containing the number of occurrences
    # of A, B, X, and Y, in that order.

    numa = numb = numx = numy = 0
    substrings = operation.split("*")
    first = True
    resultSize = [1, 1]
    for s in substrings:
        s = s.lower()
        if (s == "a") or (s == "trans(a)") or (s == "ctrans(a)"):
            numa += 1
        elif (s == "b") or (s == "trans(b)") or (s == "ctrans(b)"):
            numb += 1
        elif (s == "x") or (s == "trans(x)") or (s == "ctrans(x)"):
            numx += 1
        elif (s == "y") or (s == "trans(y)") or (s == "ctrans(y)"):
            numy += 1
    return [numa, numb, numx, numy]


def matMulResultSize(operation, arows, acols, brows, bcols, nx, ny):
    # Calculate the size of the returned array based on a
    #    matrix multiplication.

    # The size of the returned array is based on the input (operation) string.
    # The string, which is delimited by asterisks, can contain any of
    # the following substrings:

    #   A, B, x, y
    #   trans(A), trans(B), trans(x), trans(y)
    #   ctrans(A), ctrans(B), ctrans(x), ctrans(y)

    # Multiplying two matrices with size nrow1*ncol1, nrow2,ncol2
    #    creates a new matrix with size nrow1*ncol2.

    substrings = operation.split("*")
    first = True
    resultSize = [1, 1]
    for s in substrings:
        s = s.lower()
        if (s == "a"):
            arraySize = [arows, acols]
        elif (s == "trans(a)") or (s == "ctrans(a)"):
            arraySize = [acols, arows]
        elif (s == "b"):
            arraySize = [brows, bcols]
        elif (s == "trans(b)") or (s == "ctrans(b)"):
            arraySize = [bcols, brows]
        elif (s == "x"):
            arraySize = [nx, 1]
        elif (s == "trans(x)") or (s == "ctrans(x)"):
            arraySize = [1, nx]
        elif (s == "y"):
            arraySize = [ny, 1]
        elif (s == "trans(y)") or (s == "ctrans(y)"):
            arraySize = [1, ny]
        if (first):
            resultSize = arraySize
            first = False
        else:
            resultSize = [resultSize[0], arraySize[1]]

    return resultSize
