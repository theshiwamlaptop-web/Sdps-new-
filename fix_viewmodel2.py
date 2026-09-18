import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    text = f.read()

pattern1 = r'val auth = com\.google\.firebase\.auth\.FirebaseAuth\.getInstance\(\)'
replacement1 = 'val auth = null // com.google.firebase.auth.FirebaseAuth.getInstance()'
text = re.sub(pattern1, replacement1, text)

pattern2 = r'android\.util\.Log\.d\("SchoolViewModel", "Adding student: \$\{student\.name\}, FirebaseAuth current user: \$\{com\.google\.firebase\.auth\.FirebaseAuth\.getInstance\(\)\.currentUser\?\.uid\}"\)'
replacement2 = 'android.util.Log.d("SchoolViewModel", "Adding student: ${student.name}")'
text = re.sub(pattern2, replacement2, text)

# For sendPasswordReset, if auth is null, we need to handle it.
# Actually, wait, if I replace `val auth = ...` with `val auth = null`, `auth.sendPasswordResetEmail(clean)` will give a compiler error since it's a null object.

