# Copyright (c) 2018 Advanced Micro Devices, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
from nnir import *

def main():
    usage = 'Usage: python nnir-update.py [--batch-size <n>] [--fuse-ops 0|1] [--slice-groups 0|1] <nnirInputFolder> <nnirOutputFolder>'
    batchSize = 0
    fuseOps = False
    sliceGroups = False
    pos = 1
    while len(sys.argv[pos:]) >= 2 and sys.argv[pos][:2] == '--':
        if sys.argv[pos] == '--batch-size':
            batchSize = int(sys.argv[pos+1])
            pos = pos + 2
        elif sys.argv[pos] == '--fuse-ops':
            fuseOps = False if int(sys.argv[pos+1]) == 0 else True
            pos = pos + 2
        elif sys.argv[pos] == '--slice-groups':
            sliceGroups = False if int(sys.argv[pos+1]) == 0 else True
            pos = pos + 2
        else:
            print('ERROR: invalid option: %s' % (sys.argv[pos]))
            print(usage)
            sys.exit(1)
    if len(sys.argv[pos:]) != 2:
        print(usage)
        sys.exit(1)
    inputFolder = sys.argv[pos]
    outputFolder = sys.argv[pos+1]
    print('reading IR model from ' + inputFolder + ' ...')
    graph = IrGraph()
    graph.fromFile(inputFolder)
    if batchSize > 0:
        graph.updateBatchSize(batchSize)
    if sliceGroups:
        graph.sliceGroups()
    if fuseOps:
        graph.fuseOps()
    print('writing IR model into ' + outputFolder + ' ...')
    graph.toFile(outputFolder)

if __name__ == '__main__':
    main()
