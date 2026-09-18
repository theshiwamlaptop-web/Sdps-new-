import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    text = f.read()

pattern = r'fun sendPasswordReset\(destination: String, onSuccess: \(\) -> Unit, onFailure: \(String\) -> Unit\) \{[\s\S]*?addOnCompleteListener \{ task ->[\s\S]*?\}\n                    \}\n                \}\n            \} catch \(e: Exception\) \{'

replacement = """fun sendPasswordReset(destination: String, onSuccess: () -> Unit, onFailure: (String) -> Unit) {
        viewModelScope.launch {
            _isAuthenticating.value = true
            try {
                val clean = destination.trim()
                // Simulated reset
                kotlinx.coroutines.delay(1000)
                if (clean.contains("@")) {
                    onSuccess()
                } else {
                    val phoneDigits = clean.filter { it.isDigit() }
                    if (phoneDigits.length != 10) {
                        throw Exception("कृपया 10 अंकों का मान्य फ़ोन नंबर दर्ज करें!")
                    }
                    val user = repository.findUserByPhone(phoneDigits)
                    if (user == null || user.email.isEmpty()) {
                        throw Exception("यह फ़ोन नंबर किसी भी उपयोगकर्ता से लिंक नहीं है!")
                    }
                    onSuccess()
                }
            } catch (e: Exception) {"""

new_text = re.sub(pattern, replacement, text)

# Also fix the line with FirebaseAuth in addOrUpdateStudent
new_text = new_text.replace('android.util.Log.d("SchoolViewModel", "Adding student: ${student.name}, FirebaseAuth current user: ${com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.uid}")', 'android.util.Log.d("SchoolViewModel", "Adding student: ${student.name}")')

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(new_text)

