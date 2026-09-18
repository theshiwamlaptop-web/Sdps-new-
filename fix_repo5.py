import re

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    text = f.read()

text = text.replace(
    'fs.collection("users").document(user.userId).set(updatedUser)',
    'kotlinx.coroutines.withTimeout(5000) { fs.collection("users").document(user.userId).set(updatedUser).await() }'
)
text = text.replace(
    'fs.collection("users").document(user.userId).set(user)',
    'kotlinx.coroutines.withTimeout(5000) { fs.collection("users").document(user.userId).set(user).await() }'
)

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write(text)
