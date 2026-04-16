[app]
title = CheckSheet
package.name = checksheetapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,xlsx,json
version = 1.0

# [최적화] 필수 라이브러리
requirements = python3,kivy,openpyxl,et_xmlfile,jdcal,pyjnius,android,pysmb,pyasn1,six

orientation = portrait
fullscreen = 0

# [권한]
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# [네이티브 PDF 라이브러리] - 2.8.2 버전 유지
android.gradle_dependencies = com.github.barteksc:android-pdf-viewer:2.8.2

# [중요] AndroidX 및 Jetifier 활성화 (크래시 방지 핵심)
android.enable_androidx = True
android.gradle_options = android.useAndroidX=true, android.enableJetifier=true

# [빌드 가속 및 메모리 설정] - 빌드 멈춤 방지
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# Android API 설정
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
