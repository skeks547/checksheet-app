[app]
title = PDFTestFinal
package.name = pdftestfinal
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,pdf
source.exclude_dirs = backup, bin, .buildozer
version = 1.0

requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# [해결] 가장 검증된 안정 버전(2.8.2) 사용
android.gradle_dependencies = com.github.mhiew:android-pdf-viewer:2.8.2
android.gradle_repositories = https://jitpack.io

android.enable_androidx = True
android.accept_sdk_license = True

# [해결] 빌드 성공률이 가장 높은 API 레벨 선택
android.api = 31
android.minapi = 21
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 0
