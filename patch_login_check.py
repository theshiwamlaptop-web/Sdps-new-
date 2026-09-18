import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

bad_login = '''    override suspend fun login(userId: String, role: String, fullname: String, password: String): Result<User> {
        return try {
            val processedId = userId.trim()'''

good_login = '''    override suspend fun login(userId: String, role: String, fullname: String, password: String): Result<User> {
        return try {
            // Verify FirebaseApp and FirebaseAuth before login
            val hasApps = com.google.firebase.FirebaseApp.getApps(context).isNotEmpty()
            if (!hasApps) {
                android.util.Log.e("SchoolRepository", "FirebaseApp is not initialized before login!")
            }
            if (firebaseAuth == null) {
                android.util.Log.e("SchoolRepository", "FirebaseAuth is null before login!")
            }

            val processedId = userId.trim()'''

content = content.replace(bad_login, good_login)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
print("Patched login check.")
