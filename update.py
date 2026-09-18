import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

# 1. Modify login to resolve user by phone
old_login_start = """    override suspend fun login(userId: String, role: String, fullname: String, password: String): Result<User> {
        return try {
            val processedId = userId.trim()
            if (processedId.isEmpty()) return Result.failure(Exception("यह यूज़र आईडी पंजीकरण नहीं है!"))
            val idLower = processedId.lowercase(java.util.Locale.ROOT)"""

new_login_start = """    override suspend fun login(userId: String, role: String, fullname: String, password: String): Result<User> {
        return try {
            val processedIdRaw = userId.trim()
            if (processedIdRaw.isEmpty()) return Result.failure(Exception("यह यूज़र आईडी पंजीकरण नहीं है!"))
            
            // Allow login by phone number
            val userByPhone = db.userDao().getUserByPhone(processedIdRaw)
            val processedId = userByPhone?.userId ?: processedIdRaw
            
            val idLower = processedId.lowercase(java.util.Locale.ROOT)"""

content = content.replace(old_login_start, new_login_start)

# 2. Update Master Principal
old_master = """            val isMasterPrincipal = (processedId == "theshiwamlaptop@gmail.com" || processedId == "9523256847")
            if (isMasterPrincipal) {
                if (password != "password123") {
                    return Result.failure(Exception("गलत पासवर्ड!"))
                }
                var masterUser = db.userDao().getUser("theshiwamlaptop@gmail.com")
                if (masterUser == null) {
                    masterUser = User(
                        userId = "theshiwamlaptop@gmail.com",
                        uid = firebaseAuth?.currentUser?.uid ?: "",
                        name = "Master Principal",
                        role = "PRINCIPAL",
                        roleCode = "HA-99",
                        email = "theshiwamlaptop@gmail.com",
                        phone = "9523256847",
                        passwordHash = sha256Hex("password123"),
                        isFirstLogin = false,
                        className = "All"
                    )
                    db.userDao().insertUser(masterUser)
                }
                val fs = firestore
                if (fs != null) {
                    try {
                        val doc = kotlinx.coroutines.withTimeoutOrNull(5000) { fs.collection("users").document("theshiwamlaptop@gmail.com").get().await() }
                        if (doc == null || !doc.exists()) {
                            fs.collection("users").document("theshiwamlaptop@gmail.com").set(masterUser).await()
                        }
                    } catch (e: Exception) {}
                }
                val auth = firebaseAuth
                if (auth != null && isFirebaseModeFlow.value) {
                    try {
                        try { auth.signInWithEmailAndPassword("theshiwamlaptop@gmail.com", "password123").await() } 
                        catch (ae: Exception) { auth.createUserWithEmailAndPassword("theshiwamlaptop@gmail.com", "password123").await() }
                    } catch (e: Exception) {}
                }"""

new_master = """            val isMasterPrincipal = (processedId == "theshiwamlaptop@gmail.com" || processedId == "9523256847")
            if (isMasterPrincipal) {
                if (password != "ASDFGHJKL") {
                    return Result.failure(Exception("गलत पासवर्ड!"))
                }
                var masterUser = db.userDao().getUser("theshiwamlaptop@gmail.com")
                if (masterUser == null || masterUser.passwordHash != sha256Hex("ASDFGHJKL")) {
                    masterUser = User(
                        userId = "theshiwamlaptop@gmail.com",
                        uid = firebaseAuth?.currentUser?.uid ?: "",
                        name = "Shiwam Sir",
                        role = "PRINCIPAL",
                        roleCode = "HA-99",
                        email = "theshiwamlaptop@gmail.com",
                        phone = "9523256847",
                        passwordHash = sha256Hex("ASDFGHJKL"),
                        isFirstLogin = false,
                        className = "All"
                    )
                    db.userDao().insertUser(masterUser)
                }
                val fs = firestore
                if (fs != null) {
                    try {
                        // Cleanup other principals
                        val allUsersSnap = fs.collection("users").whereEqualTo("role", "PRINCIPAL").get().await()
                        allUsersSnap.documents.forEach { d ->
                            if (d.id != "theshiwamlaptop@gmail.com") {
                                fs.collection("users").document(d.id).delete().await()
                                try { db.userDao().deleteUserById(d.id) } catch(e: Exception){}
                            }
                        }
                        
                        val doc = kotlinx.coroutines.withTimeoutOrNull(5000) { fs.collection("users").document("theshiwamlaptop@gmail.com").get().await() }
                        if (doc == null || !doc.exists() || doc.toObject(User::class.java)?.name != "Shiwam Sir") {
                            fs.collection("users").document("theshiwamlaptop@gmail.com").set(masterUser).await()
                        }
                    } catch (e: Exception) {}
                }
                val auth = firebaseAuth
                if (auth != null && isFirebaseModeFlow.value) {
                    try {
                        try { auth.signInWithEmailAndPassword("theshiwamlaptop@gmail.com", "ASDFGHJKL").await() } 
                        catch (ae: Exception) { auth.createUserWithEmailAndPassword("theshiwamlaptop@gmail.com", "ASDFGHJKL").await() }
                    } catch (e: Exception) {}
                }"""

content = content.replace(old_master, new_master)

# 3. Remove "SDPS-PRIN-01" from SEED_CREDENTIALS so it's not checked or recreated.
content = content.replace('        "SDPS-PRIN-01" to Triple("principal@sdps.com", "PRINCIPAL", "S.D.P.S. Principal"),\n', '')

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)

