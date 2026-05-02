[app]

# (str) Title of your application
title = Age Calculator

# (str) Package name
package.name = agecalculator

# (str) Package domain (needed for android/ios packaging)
package.domain = org.auraway

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (Added json for your settings.json)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, venv, .kivy

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Updated to your specific versions. 'datetime' is built-in but listed for safety.
requirements = python3, kivy==2.3.1, kivymd==1.2.0, datetime

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API (33 is standard for modern apps)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) Enable AndroidX support (Required for KivyMD 1.2.0)
android.enable_androidx = True

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

[buildozer]

# (int) Log level (2 = debug, shows all errors during build)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
