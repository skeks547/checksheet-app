[app]
title = PDFQuickTest
package.name = pdfqtest
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,pdf
source.exclude_dirs = backup, bin, .buildozer
version = 0.3

# [핵심] 최소 요구사항
requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

# [핵심] 권한
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# [핵심] Gradle 의존성 및 AndroidX
android.gradle_dependencies = com.github.barteksc:android-pdf-viewer:3.2.0-beta.1
android.enable_androidx = True

# 빌드 환경
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
