import re

with open("app/src/main/java/com/example/ui/screens/PremiumLoginScreen.kt", "r") as f:
    content = f.read()

target_lottie = """        // Lottie Mascot
        val composition by rememberLottieComposition(LottieCompositionSpec.RawRes(R.raw.login_character))"""

replacement_lottie = """        // Lottie Mascot
        val compositionResult = rememberLottieComposition(LottieCompositionSpec.RawRes(R.raw.login_character))
        val composition by compositionResult"""

content = content.replace(target_lottie, replacement_lottie)

target_lottie_anim = """                    LottieAnimation(
                        composition = composition,
                        progress = { progress },
                        modifier = Modifier
                            .size(120.dp)
                            .padding(bottom = 16.dp)
                    )"""

replacement_lottie_anim = """                    if (compositionResult.isFailure) {
                        // Fallback static UI if animation fails to load
                        Icon(
                            imageVector = Icons.Filled.Lock,
                            contentDescription = "Login",
                            modifier = Modifier
                                .size(100.dp)
                                .padding(bottom = 16.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                    } else {
                        LottieAnimation(
                            composition = composition,
                            progress = { progress },
                            modifier = Modifier
                                .size(120.dp)
                                .padding(bottom = 16.dp)
                        )
                    }"""

content = content.replace(target_lottie_anim, replacement_lottie_anim)

with open("app/src/main/java/com/example/ui/screens/PremiumLoginScreen.kt", "w") as f:
    f.write(content)
