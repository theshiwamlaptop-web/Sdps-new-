import os

path = '/app/applet/app/src/main/java/com/example/data/repository/SchoolRepository.kt'
with open(path, 'r') as f:
    content = f.read()

# Replace 1
bad1 = """                } catch (e: Exception) {
                    val errorMsg = e.message ?: ""
                    val isNetworkIssue = e is com.google.firebase.FirebaseNetworkException || 
                                         errorMsg.contains("network") || errorMsg.contains("offline") || errorMsg.contains("timed out")
                    if (!isNetworkIssue) {"""

good1 = """                } catch (e: Exception) {
                    val errorMsg = e.message ?: ""
                    android.util.Log.e("SchoolRepository", "Firebase Auth login failed: $errorMsg", e)
                    val isNetworkIssue = e is com.google.firebase.FirebaseNetworkException || 
                                         errorMsg.contains("network") || errorMsg.contains("offline") || errorMsg.contains("timed out") || e is com.google.firebase.FirebaseApiNotAvailableException
                    if (!isNetworkIssue) {"""

content = content.replace(bad1, good1)

# Replace 2
bad2 = """        } catch (e: Exception) {
            Result.failure(Exception(e.message ?: "गलत यूज़र आईडी या पासवर्ड!"))
        }"""
good2 = """        } catch (e: Exception) {
            android.util.Log.e("SchoolRepository", "Login flow exception: ${e.message}", e)
            Result.failure(Exception(e.message ?: "गलत यूज़र आईडी या पासवर्ड!"))
        }"""

content = content.replace(bad2, good2)

with open(path, 'w') as f:
    f.write(content)
print("done")
