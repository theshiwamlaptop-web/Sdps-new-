import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

bad_throw = '''                    if (!isNetworkIssue) {
                        try {
                            auth.createUserWithEmailAndPassword(email, password).await()
                            firebaseAuthSuccess = true
                            createdJustNow = true
                        } catch (createEx: Exception) {
                            Log.w("SchoolRepository", "Auth creation fallback failed: ${createEx.message}")
                        }
                    }
                }
            }
            
            // Try fetching from Firestore if authenticated (which implies rules will allow it)'''

good_throw = '''                    if (!isNetworkIssue) {
                        try {
                            auth.createUserWithEmailAndPassword(email, password).await()
                            firebaseAuthSuccess = true
                            createdJustNow = true
                        } catch (createEx: Exception) {
                            Log.w("SchoolRepository", "Auth creation fallback failed: ${createEx.message}")
                        }
                    }
                }
            }
            
            // THROW DEBUG LOGS FOR PROOF
            return Result.failure(Exception(debugLogs.toString()))
            
            // Try fetching from Firestore if authenticated (which implies rules will allow it)'''

content = content.replace(bad_throw, good_throw)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
print("Added throw for debug logs.")
