import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

bad_teacher = '''                    db.userDao().insertUser(dbUser)
                    _currentUser.value = dbUser
                    return dbUser
                }
            }'''
good_teacher = '''                    db.userDao().insertUser(dbUser)
                    _currentUser.value = dbUser
                    
                    val auth = firebaseAuth
                    if (auth != null && isFirebaseModeFlow.value && auth.currentUser == null) {
                        try {
                            try { auth.signInWithEmailAndPassword("$lastUserId@sdps.com", "tchr123").await() } 
                            catch (ae: Exception) { auth.createUserWithEmailAndPassword("$lastUserId@sdps.com", "tchr123").await() }
                        } catch (e: Exception) {
                            android.util.Log.e("SchoolRepository", "Failed to restore Firebase Auth for teacher", e)
                        }
                    }
                    startBackgroundFirebaseSync()
                    return dbUser
                }
            }'''

content = content.replace(bad_teacher, good_teacher)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
print("Patched teacher restore.")
