import sys as sys
import os

### INCLUDE LOCAL PACKAGE DIRECTORIES
cwd = os.getcwd()
print('Current working directory: ', cwd)

drawing_subdirectory = os.path.join(cwd, 'drawing')
memory_diagrams_subdirectory = os.path.join(cwd, 'memory_diagrams')

# Should be refactored soon into a single function call
sys.path.append(drawing_subdirectory)
sys.path.append(memory_diagrams_subdirectory)

import timelapse as timelapse
import sparse as sparse
import memory_diagrams.array as array
import memory_diagrams.hybrid as hybrid

### BEGIN SCRIPT

array = array.Array(10)
array.Add(1)
array.Add(2)
array.Add(3)
array.Add(4)
array.Add(5)
array.Add(6)

array.Draw()

# TODO: Fix
# array.Save(name = 'image_1a.png')

# timelapse = timelapse.Timelapse(16)
# timelapse.Draw()
