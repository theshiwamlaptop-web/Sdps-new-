import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

bad_net = '''            fun isNetworkAvailable(): Boolean {
                val connectivityManager = context.getSystemService(android.content.Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
                val network = connectivityManager.activeNetwork ?: return false
                val activeNetwork = connectivityManager.getNetworkCapabilities(network) ?: return false
                return activeNetwork.hasCapability(android.net.NetworkCapabilities.NET_CAPABILITY_INTERNET)
            }
            
            val isOnline = isNetworkAvailable()
            if (!isOnline) {
                android.util.Log.w("SchoolRepository", "No internet connection detected. Proceeding with offline Room login flow.")
            }'''

good_net = '''            fun isNetworkAvailable(): Boolean {
                val connectivityManager = context.getSystemService(android.content.Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
                val network = connectivityManager.activeNetwork ?: run {
                    android.util.Log.d("DEBUG_NET", "network is null")
                    return false
                }
                val activeNetwork = connectivityManager.getNetworkCapabilities(network) ?: run {
                    android.util.Log.d("DEBUG_NET", "activeNetwork is null")
                    return false
                }
                val hasInternet = activeNetwork.hasCapability(android.net.NetworkCapabilities.NET_CAPABILITY_INTERNET)
                android.util.Log.d("DEBUG_NET", "hasCapability: $hasInternet")
                return hasInternet
            }
            
            val isOnline = isNetworkAvailable()
            android.util.Log.d("DEBUG_NET", "isOnline = $isOnline")
            if (!isOnline) {
                android.util.Log.w("SchoolRepository", "No internet connection detected. Proceeding with offline Room login flow.")
            }'''

content = content.replace(bad_net, good_net)


bad_auth = '''            // Attempt Firebase Auth Flow first to bypass Security Rule blocks
            if (auth != null && isFirebaseModeFlow.value && isOnline) {
                try {
                    val authResult = auth.signInWithEmailAndPassword(email, password).await()
                    if (authResult.user != null) {
                        firebaseAuthSuccess = true
                    }
                } catch (e: Exception) {'''

good_auth = '''            // Attempt Firebase Auth Flow first to bypass Security Rule blocks
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

content = content.replace(bad_auth, good_auth)

bad_sync = '''        // 1. Students Synchronization Listeners
        try {
            val listener = fs.collection("students").addSnapshotListener { snapshot, error ->
                if (error != null) {
                    Log.e("SchoolRepository", "Firestore Synclist Error [students]: ${error.message}", error)
                    
                    return@addSnapshotListener
                }'''

good_sync = '''        // 1. Students Synchronization Listeners
        try {
            val listener = fs.collection("students").addSnapshotListener { snapshot, error ->
                android.util.Log.d("DEBUG_NET", "SnapshotListener [students] triggered, error: ${error?.message}")
                if (error != null) {
                    Log.e("SchoolRepository", "Firestore Synclist Error [students]: ${error.message}", error)
                    
                    return@addSnapshotListener
                }'''

content = content.replace(bad_sync, good_sync)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
print("Patched.")
