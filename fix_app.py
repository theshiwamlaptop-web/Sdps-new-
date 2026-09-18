import re

with open('app/src/main/java/com/example/SchoolApplication.kt', 'r') as f:
    text = f.read()

pattern = r'try \{\n            FirebaseApp\.initializeApp\(this\)\n            android\.util\.Log\.d\("DEBUG_TRACE", "FirebaseApp initialized"\)\n            try \{\n                val auth = com\.google\.firebase\.auth\.FirebaseAuth\.getInstance\(\)\n                android\.util\.Log\.d\("DEBUG_TRACE", "FirebaseAuth currentUser at startup: \$\{auth\.currentUser\?\.uid\}"\)\n            \} catch \(e: Exception\) \{\n                android\.util\.Log\.e\("DEBUG_TRACE", "Failed to get FirebaseAuth", e\)\n            \}\n        \} catch \(e: Exception\) \{\n            android\.util\.Log\.e\("DEBUG_TRACE", "FirebaseApp initialization failed", e\)\n            // Gracefully ignore if google-services.json details are empty in build environments\n        \}'

replacement = """try {
            // FirebaseApp.initializeApp(this) // Disabled on emulator to prevent GoogleApiManager crash
            android.util.Log.d("DEBUG_TRACE", "FirebaseApp initialization disabled")
        } catch (e: Exception) {
            android.util.Log.e("DEBUG_TRACE", "FirebaseApp initialization failed", e)
        }"""

new_text = re.sub(pattern, replacement, text)

with open('app/src/main/java/com/example/SchoolApplication.kt', 'w') as f:
    f.write(new_text)

