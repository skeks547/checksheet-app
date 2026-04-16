[app]
title = PDFTest
package.name = pdftest
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,pdf
version = 0.1

# 최소화된 요구사항 (PDF 테스트 전용)
requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

# 권한
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# 가장 안정적인 PDF 라이브러리 설정 (JitPack 이용)
android.gradle_dependencies = com.github.barteksc:android-pdf-viewer:2.8.2
android.gradle_repositories = https://jitpack.io

# 필수 설정
android.enable_androidx = True
android.accept_sdk_license = True
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 0
