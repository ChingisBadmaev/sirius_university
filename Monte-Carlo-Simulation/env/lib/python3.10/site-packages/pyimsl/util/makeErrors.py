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
import io
# copy the new versions of imslerr.* and imsls_e.* from your CNL
# installation along with this script to your
# imsl/locale/en/LC_MESSAGES directory and run it:
#
# python3 makeErrors.py
#
# it will spit out the mathErrors.py and statErrors.py files
# into that dir. Move or copy them to the appropriate imsl/math or
# imsl/stat directory and you're ready to go...
#
copyright = """
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
""".lstrip()

files = ["imslerr.dat", "imsls_e.dat"]

for file in files:
    input = open(file, mode='rt')
    lines = []

    for line in input:
        tmpline = line.split()
        if len(tmpline) != 0 and tmpline[0].isdigit():
            tmpline1 = "{:<34}=  {}\n".format(tmpline[1], tmpline[0])
            lines.append(tmpline1)
    if file == "imslerr.dat":
        output = open("mathErrors.py", mode="wt")
    else:
        output = open("statErrors.py", mode="wt")
    output.writelines(copyright)
    output.writelines(lines)
    output.close()
    input.close()
