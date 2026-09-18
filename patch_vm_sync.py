import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    content = f.read()

bad_impl = '''    // Backend Connection
    val isFirebaseMode = repository.isFirebaseModeFlow'''

good_impl = '''    // Backend Connection
    val isFirebaseMode = repository.isFirebaseModeFlow

    fun forceSync() {
        repository.forceSync()
    }'''
content = content.replace(bad_impl, good_impl)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(content)
