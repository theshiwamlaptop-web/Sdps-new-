import re

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    content = f.read()

if "import androidx.room.withTransaction" not in content:
    content = content.replace("import kotlinx.coroutines.launch", "import kotlinx.coroutines.launch\nimport androidx.room.withTransaction")

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write(content)

