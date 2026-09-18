import os

filepath = "app/src/main/java/com/example/ui/screens/PremiumLoginScreen.kt"
with open(filepath, "r") as f:
    content = f.read()

# Add imports
imports = """import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.ui.draw.scale
"""

content = content.replace("import androidx.compose.ui.draw.clip", imports + "import androidx.compose.ui.draw.clip")

# Fix ElevatedCard
target_card = """            ElevatedCard(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .wrapContentHeight()
                    .padding(vertical = 16.dp),
                shape = RoundedCornerShape(32.dp),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 20.dp),
                colors = CardDefaults.elevatedCardColors(
                    containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.96f)
                )
            ) {"""

replacement_card = """            ElevatedCard(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .wrapContentHeight()
                    .padding(vertical = 24.dp)
                    .border(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f), RoundedCornerShape(32.dp)),
                shape = RoundedCornerShape(32.dp),
                elevation = CardDefaults.elevatedCardElevation(defaultElevation = 24.dp),
                colors = CardDefaults.elevatedCardColors(
                    containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.85f)
                )
            ) {"""

content = content.replace(target_card, replacement_card)

# Fix Button 1 (Standard Login)
target_btn1 = """                                Button(
                                    onClick = {
                                        focusManager.clearFocus()
                                        viewModel.loginUser(userId, selectedRole, "", password)
                                    },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(52.dp),
                                    shape = RoundedCornerShape(12.dp),
                                    enabled = !isAuthenticating && userId.isNotBlank() && password.isNotBlank()
                                ) {"""

replacement_btn1 = """                                val interactionSource = remember { MutableInteractionSource() }
                                val isPressed by interactionSource.collectIsPressedAsState()
                                val scale by animateFloatAsState(if (isPressed) 0.95f else 1f, label = "btnScale")
                                Button(
                                    onClick = {
                                        focusManager.clearFocus()
                                        viewModel.loginUser(userId, selectedRole, "", password)
                                    },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(56.dp)
                                        .scale(scale),
                                    shape = RoundedCornerShape(16.dp),
                                    enabled = !isAuthenticating && userId.isNotBlank() && password.isNotBlank(),
                                    interactionSource = interactionSource
                                ) {"""
content = content.replace(target_btn1, replacement_btn1)

# Fix Button 2 (OTP verify)
target_btn2 = """                                    Button(
                                        onClick = {
                                            focusManager.clearFocus()
                                            viewModel.verifyOtpAndLogin(verificationId, otpCode, phoneInput)
                                        },
                                        modifier = Modifier.fillMaxWidth().height(52.dp),
                                        shape = RoundedCornerShape(12.dp),
                                        enabled = !isAuthenticating && otpCode.isNotBlank()
                                    ) {"""

replacement_btn2 = """                                    val otpInteractionSource = remember { MutableInteractionSource() }
                                    val isOtpPressed by otpInteractionSource.collectIsPressedAsState()
                                    val otpScale by animateFloatAsState(if (isOtpPressed) 0.95f else 1f, label = "otpBtnScale")
                                    Button(
                                        onClick = {
                                            focusManager.clearFocus()
                                            viewModel.verifyOtpAndLogin(verificationId, otpCode, phoneInput)
                                        },
                                        modifier = Modifier.fillMaxWidth().height(56.dp).scale(otpScale),
                                        shape = RoundedCornerShape(16.dp),
                                        enabled = !isAuthenticating && otpCode.isNotBlank(),
                                        interactionSource = otpInteractionSource
                                    ) {"""
content = content.replace(target_btn2, replacement_btn2)

# Fix Button 3 (Send OTP)
target_btn3 = """                                    Button(
                                        onClick = {
                                            focusManager.clearFocus()
                                            if (activity != null) {
                                                viewModel.startPhoneVerification(phoneInput, activity, { vId -> verificationId = vId }, { /* error */ })
                                            } else {
                                                Toast.makeText(context, "Cannot send OTP (Activity context missing)", Toast.LENGTH_SHORT).show()
                                            }
                                        },
                                        modifier = Modifier.fillMaxWidth().height(52.dp),
                                        shape = RoundedCornerShape(12.dp),
                                        enabled = !isAuthenticating && phoneInput.isNotBlank()
                                    ) {"""

replacement_btn3 = """                                    val reqInteractionSource = remember { MutableInteractionSource() }
                                    val isReqPressed by reqInteractionSource.collectIsPressedAsState()
                                    val reqScale by animateFloatAsState(if (isReqPressed) 0.95f else 1f, label = "reqBtnScale")
                                    Button(
                                        onClick = {
                                            focusManager.clearFocus()
                                            if (activity != null) {
                                                viewModel.startPhoneVerification(phoneInput, activity, { vId -> verificationId = vId }, { /* error */ })
                                            } else {
                                                Toast.makeText(context, "Cannot send OTP (Activity context missing)", Toast.LENGTH_SHORT).show()
                                            }
                                        },
                                        modifier = Modifier.fillMaxWidth().height(56.dp).scale(reqScale),
                                        shape = RoundedCornerShape(16.dp),
                                        enabled = !isAuthenticating && phoneInput.isNotBlank(),
                                        interactionSource = reqInteractionSource
                                    ) {"""
content = content.replace(target_btn3, replacement_btn3)

# Fix OutlinedTextFields shape to 16.dp instead of 12.dp
content = content.replace("shape = RoundedCornerShape(12.dp)", "shape = RoundedCornerShape(16.dp)")

with open(filepath, "w") as f:
    f.write(content)
print("Success")
