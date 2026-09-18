import re
with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

content = content.replace('android:icon="@drawable/logo_sdps"', 'android:icon="@mipmap/ic_launcher"')
content = content.replace('android:roundIcon="@drawable/logo_sdps"', 'android:roundIcon="@mipmap/ic_launcher_round"')

with open('app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
