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

### BEGIN SCRIPT

timelapse = timelapse.Timelapse(16)
timelapse.Draw()
