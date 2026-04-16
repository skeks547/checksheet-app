[app]
title = PDFTest
package.name = pdftest
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,pdf
source.exclude_dirs = backup, bin, .buildozer
version = 0.2

# 핵심 요구사항만 포함
requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

# 권한 설정
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# AndroidX 호환 라이브러리 사용
android.gradle_dependencies = com.github.barteksc:android-pdf-viewer:3.2.0-beta.1
android.enable_androidx = True

# 빌드 환경 설정
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
