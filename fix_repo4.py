with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "r") as f:
    text = f.read()

# Let's replace auth.signInWithEmailAndPassword with a timeout
text = text.replace(
    'auth.signInWithEmailAndPassword("$lastUserId@sdps.com", "tchr123").await()',
    'kotlinx.coroutines.withTimeout(5000) { auth.signInWithEmailAndPassword("$lastUserId@sdps.com", "tchr123").await() }'
)
text = text.replace(
    'val authResult = auth.signInWithEmailAndPassword(email, password).await()',
    'val authResult = kotlinx.coroutines.withTimeout(8000) { auth.signInWithEmailAndPassword(email, password).await() }'
)
text = text.replace(
    'val authResult = auth.signInWithCredential(credential).await()',
    'val authResult = kotlinx.coroutines.withTimeout(8000) { auth.signInWithCredential(credential).await() }'
)
with open("app/src/main/java/com/example/data/repository/SchoolRepository.kt", "w") as f:
    f.write(text)

