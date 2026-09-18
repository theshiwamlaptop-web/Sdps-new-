import re

with open("app/src/main/java/com/example/ui/SchoolViewModel.kt", "r") as f:
    content = f.read()

# Replace .stateIn(viewModelScope with .flowOn(kotlinx.coroutines.Dispatchers.Default).stateIn(viewModelScope
content = content.replace(".stateIn(viewModelScope", ".flowOn(kotlinx.coroutines.Dispatchers.Default)\n        .stateIn(viewModelScope")

with open("app/src/main/java/com/example/ui/SchoolViewModel.kt", "w") as f:
    f.write(content)
