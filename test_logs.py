import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

bad_login = '''            val isOnline = isNetworkAvailable()
            android.util.Log.d("DEBUG_NET", "isOnline = $isOnline")
            if (!isOnline) {
                android.util.Log.w("SchoolRepository", "No internet connection detected. Proceeding with offline Room login flow.")
            }
            
            android.util.Log.d("DEBUG_NET", "auth!=null: ${auth != null}, isFirebaseModeFlow: ${isFirebaseModeFlow.value}")
            if (auth != null && isFirebaseModeFlow.value && isOnline) {
                try {
                    android.util.Log.d("DEBUG_NET", "calling signInWithEmailAndPassword")
                    val authResult = auth.signInWithEmailAndPassword(email, password).await()
                    if (authResult.user != null) {
                        firebaseAuthSuccess = true
                        android.util.Log.d("DEBUG_NET", "signInWithEmailAndPassword success uid: ${authResult.user?.uid}")
                    }
                } catch (e: Exception) {
                    android.util.Log.e("DEBUG_NET", "Firebase Auth login failed: ${e.message}")'''

good_login = '''            val debugLogs = StringBuilder()
            val isOnline = isNetworkAvailable()
            debugLogs.append("isNetworkAvailable(): $isOnline\\n")
            
            if (!isOnline) {
                android.util.Log.w("SchoolRepository", "No internet connection detected. Proceeding with offline Room login flow.")
            }
            
            debugLogs.append("FirebaseAuth.getCurrentUser(): ${auth?.currentUser?.uid}\\n")
            debugLogs.append("auth != null && isFirebaseModeFlow.value: ${auth != null && isFirebaseModeFlow.value}\\n")
            
            if (auth != null && isFirebaseModeFlow.value && isOnline) {
                try {
                    debugLogs.append("auth.signInWithEmailAndPassword() execution: Started\\n")
                    val authResult = auth.signInWithEmailAndPassword(email, password).await()
                    if (authResult.user != null) {
                        firebaseAuthSuccess = true
                        debugLogs.append("auth.signInWithEmailAndPassword() execution: Success (${authResult.user?.uid})\\n")
                    }
                } catch (e: Exception) {
                    debugLogs.append("auth.signInWithEmailAndPassword() execution: Failed (${e.message})\\n")
                    android.util.Log.e("DEBUG_NET", "Firebase Auth login failed: ${e.message}")'''

content = content.replace(bad_login, good_login)

bad_sync = '''        // 1. Students Synchronization Listeners
        try {
            val listener = fs.collection("students").addSnapshotListener { snapshot, error ->
                android.util.Log.d("DEBUG_NET", "SnapshotListener [students] triggered, error: ${error?.message}")
                if (error != null) {
                    Log.e("SchoolRepository", "Firestore Synclist Error [students]: ${error.message}", error)
                    
                    return@addSnapshotListener
                }'''

good_sync = '''        // 1. Students Synchronization Listeners
        try {
            val listener = fs.collection("students").addSnapshotListener { snapshot, error ->
                android.util.Log.d("DEBUG_NET", "SnapshotListener [students] triggered, error: ${error?.message}")
                // Store the error in a global variable or emit it so we can read it.
                // For now we will just log it. If we need to prove it, we can throw it.
                if (error != null) {
                    Log.e("SchoolRepository", "Firestore Synclist Error [students]: ${error.message}", error)
                    
                    return@addSnapshotListener
                }'''

content = content.replace(bad_sync, good_sync)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
print("Patched for UI logs.")
