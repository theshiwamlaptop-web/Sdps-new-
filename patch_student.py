import re

filepath = 'app/src/main/java/com/example/data/model/Models.kt'
with open(filepath, 'r') as f:
    content = f.read()

replacement = """    val deletedBy: String = "",
    val deletedAt: String = "",
    val lastModifiedBy: String = "",
    val lastModifiedAt: String = "",
    val auditLog: String = ""
)"""
content = content.replace('    val deletedBy: String = "",\n    val deletedAt: String = "\n)', replacement)
# let's do it using regex to be safe
content = re.sub(r'val deletedBy: String = "",\s*val deletedAt: String = ""\s*\)', replacement, content)

with open(filepath, 'w') as f:
    f.write(content)
