import re

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'r') as f:
    content = f.read()

scaffold_start = """
    // Prevent the user from going back to Login/Splash if authenticated
    BackHandler(enabled = currentScreen != AppScreen.LOGIN) {
        if (currentScreen != AppScreen.DASHBOARD) {
            currentScreen = AppScreen.DASHBOARD
        } else {
            val activity = context as? android.app.Activity
            activity?.finish()
        }
    }

    if (isSessionChecking || currentScreen == AppScreen.SPLASH) {
        SplashScreen()
    } else {
        val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior(rememberTopAppBarState())
        Scaffold(
            modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
            topBar = {
"""

content = re.sub(
    r'\s*// Prevent the user from going back.*?Scaffold\(\s*topBar = \{',
    scaffold_start,
    content,
    flags=re.DOTALL
)

# And inject scrollBehavior into TopAppBar
top_app_bar_repl = """TopAppBar(
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                        titleContentColor = MaterialTheme.colorScheme.onPrimary,
                        navigationIconContentColor = MaterialTheme.colorScheme.onPrimary,
                        actionIconContentColor = MaterialTheme.colorScheme.onPrimary,
                        scrolledContainerColor = MaterialTheme.colorScheme.primary
                    ),
                    scrollBehavior = scrollBehavior,"""

content = content.replace("""TopAppBar(
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                        titleContentColor = MaterialTheme.colorScheme.onPrimary,
                        navigationIconContentColor = MaterialTheme.colorScheme.onPrimary,
                        actionIconContentColor = MaterialTheme.colorScheme.onPrimary
                    ),""", top_app_bar_repl)

with open('app/src/main/java/com/example/ui/screens/SchoolAppScreens.kt', 'w') as f:
    f.write(content)

