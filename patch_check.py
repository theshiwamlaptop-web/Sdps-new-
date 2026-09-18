import re

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    content = f.read()

content = content.replace(
"""            .addOnFailureListener { e ->
                Log.e("SchoolRepository", "⚠️ Firestore connection status check returned non-critical warning (could be offline mode, cold-start delay, or security database rules restriction): ${e.message}", e)
            }""",
"""            .addOnFailureListener { e ->
                if (firebaseAuth?.currentUser != null) {
                    Log.e("SchoolRepository", "⚠️ Firestore connection status check returned non-critical warning (could be offline mode, cold-start delay, or security database rules restriction): ${e.message}", e)
                } else {
                    Log.i("SchoolRepository", "⚠️ Firestore connection blocked (expected, user is unauthenticated).")
                }
            }""")

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write(content)
