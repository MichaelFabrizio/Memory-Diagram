import sys as sys
import os

# Starting logic
cwd = os.getcwd()

drawing_subdirectory = os.path.join(cwd, 'drawing')
memory_diagrams_subdirectory = os.path.join(cwd, 'memory_diagrams')

sys.path.append(drawing_subdirectory)
sys.path.append(memory_diagrams_subdirectory)

import timelapse as timelapse
import sparse as sparse
import memory_diagrams.array as array
import memory_diagrams.hybrid as hybrid

# Begin general code tests
array = array.Array(10)
array.Add(1)
array.Add(2)
array.Add(3)
array.Add(4)
array.Add(5)
array.Draw()

# Follow the same pattern for other datastructure types:

#sparse_set = sparse.Sparse(10)
#sparse_set.Add(1)
#sparse_set.Add(2)
#sparse_set.Add(5)
#sparse_set.Draw()

# May not be useful. It was for representing memory state changes, but the documentation will need a different process for rendering graphs.

# timelapse = timelapse.Timelapse(16)
# timelapse.Draw()
