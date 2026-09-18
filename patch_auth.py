import sys

with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "r") as f:
    content = f.read()
content = content.replace(
    "suspend fun changePassword(userId: String, newPasswordHash: String): Result<Unit>",
    "suspend fun changePassword(userId: String, oldPassword: String?, newPasswordHash: String): Result<Unit>"
)
with open("app/src/main/java/com/example/data/repository/AuthRepository.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    content = f.read()
content = content.replace(
    "override suspend fun changePassword(userId: String, newPasswordHash: String): Result<Unit> {",
    "override suspend fun changePassword(userId: String, oldPassword: String?, newPasswordHash: String): Result<Unit> {"
)

# Insert applyDefaultPassword
repo_interface = """    fun toggleFirebaseMode(enabled: Boolean)
    suspend fun applyDefaultPassword(userId: String): Result<Unit>"""
content = content.replace("    fun toggleFirebaseMode(enabled: Boolean)", repo_interface)

repo_impl = """    override suspend fun applyDefaultPassword(userId: String): Result<Unit> {
        return try {
            val user = db.userDao().getUser(userId) ?: db.userDao().getUserByPhone(userId)
            if (user != null) {
                val updated = user.copy(passwordHash = sha256Hex("DefaultPassword123"), isFirstLogin = true)
                db.userDao().insertUser(updated)
                firestore?.collection("users")?.document(user.userId)?.set(updated)
                Result.success(Unit)
            } else {
                Result.failure(Exception("User not found"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
"""
content = content.replace("    override suspend fun changePassword", repo_impl + "\n    override suspend fun changePassword")

with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/SchoolViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    "fun changePassword(userId: String, newPassword: String, onSuccess: () -> Unit, onFailure: (String) -> Unit) {",
    "fun changePassword(userId: String, oldPassword: String?, newPassword: String, onSuccess: () -> Unit, onFailure: (String) -> Unit) {"
)
content = content.replace(
    "val result = repository.changePassword(userId, newPassword)",
    "val result = repository.changePassword(userId, oldPassword, newPassword)"
)

apply_default = """
    fun applyDefaultPassword(userId: String, onSuccess: () -> Unit, onFailure: (String) -> Unit) {
        viewModelScope.launch {
            val result = (repository as com.example.data.repository.SchoolRepository).applyDefaultPassword(userId)
            if (result.isSuccess) onSuccess() else onFailure(result.exceptionOrNull()?.message ?: "Failed")
        }
    }
"""
content = content.replace("    fun clearToast() { _toastMessage.value = null }", "    fun clearToast() { _toastMessage.value = null }" + apply_default)

with open("app/src/main/java/com/example/ui/SchoolViewModel.kt", "w") as f:
    f.write(content)

