import re

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'r') as f:
    text = f.read()

pattern = r'if \(resolvedUser == null\) \{\n                    _isAuthenticating\.value = false\n                    val err = "यह फोन नंबर पंजीकृत नहीं है!"\n                    onVer                // 2\. Simulate Firebase phone auth \(to avoid GMS broker crash on emulator\)\n                kotlinx\.coroutines\.delay\(1500\)\n                _isAuthenticating\.value = false\n                onCodeSent\("simulated_verification_id"\)                    \}\n                    \}\)\n                    \.build\(\)\n                \n                com\.google\.firebase\.auth\.PhoneAuthProvider\.verifyPhoneNumber\(options\)'

replacement = """if (resolvedUser == null) {
                    _isAuthenticating.value = false
                    val err = "यह फोन नंबर पंजीकृत नहीं है!"
                    onVerificationFailed(err)
                    _loginError.value = err
                    return@launch
                }
                
                // 2. Simulate Firebase phone auth (to avoid GMS broker crash on emulator)
                kotlinx.coroutines.delay(1500)
                _isAuthenticating.value = false
                onCodeSent("simulated_verification_id")"""

new_text = re.sub(pattern, replacement, text)

with open('app/src/main/java/com/example/ui/SchoolViewModel.kt', 'w') as f:
    f.write(new_text)

