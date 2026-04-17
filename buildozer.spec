[app]
title = PDFTestOnly
package.name = pdftestonly
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,pdf
source.exclude_dirs = backup, bin, .buildozer
version = 1.0

# [중요] PDF 테스트를 위한 최소 라이브러리
requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# [중요] 검증된 mhiew 라이브러리 및 Jetifier 활성화
android.gradle_dependencies = com.github.mhiew:android-pdf-viewer:3.2.0-beta.1
android.gradle_repositories = https://jitpack.io
android.enable_androidx = True
android.enable_jetifier = True

# 빌드 환경 설정
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
