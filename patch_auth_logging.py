import re

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'r') as f:
    content = f.read()

bad_catch = '''                } catch (e: Exception) {
                    val errorMsg = e.message ?: ""
                    val isNetworkIssue = e is com.google.firebase.FirebaseNetworkException ||
                                          errorMsg.contains("network") || errorMsg.contains("offline") || errorMsg.contains("timed out")
                    if (!isNetworkIssue) {'''
good_catch = '''                } catch (e: Exception) {
                    val errorMsg = e.message ?: ""
                    android.util.Log.e("SchoolRepository", "Firebase Auth login failed: $errorMsg", e)
                    val isNetworkIssue = e is com.google.firebase.FirebaseNetworkException ||
                                          errorMsg.contains("network") || errorMsg.contains("offline") || errorMsg.contains("timed out") || e is com.google.firebase.FirebaseApiNotAvailableException
                    if (!isNetworkIssue) {'''

content = content.replace(bad_catch, good_catch)

bad_final_catch = '''        } catch (e: Exception) {
            Result.failure(Exception(e.message ?: "गलत यूज़र आईडी या पासवर्ड!"))
        }'''
good_final_catch = '''        } catch (e: Exception) {
            android.util.Log.e("SchoolRepository", "Login flow exception: ${e.message}", e)
            Result.failure(Exception(e.message ?: "गलत यूज़र आईडी या पासवर्ड!"))
        }'''

content = content.replace(bad_final_catch, good_final_catch)

with open('app/src/main/java/com/example/data/repository/SchoolRepository.kt', 'w') as f:
    f.write(content)
