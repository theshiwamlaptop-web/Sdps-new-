import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

def replace_set(match):
    prefix = match.group(1)
    return prefix + '?.addOnFailureListener { e -> android.os.Handler(android.os.Looper.getMainLooper()).post { android.widget.Toast.makeText(context, "Firebase Error: ${e.message}", android.widget.Toast.LENGTH_LONG).show() } }'

content = re.sub(r'(\.set\([^\)]+\))(?!\.await|\?|\.addOn)', replace_set, content)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)

