import re
with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    content = f.read()

def repl(m):
    return m.group(0).replace("return@addSnapshotListener", "scheduleSyncRestart()\n                    return@addSnapshotListener")

new_content = re.sub(r'if \(error != null\) \{.*?return@addSnapshotListener\s*\}', repl, content, flags=re.DOTALL)
print("Replaced instances:", new_content.count("scheduleSyncRestart()"))
