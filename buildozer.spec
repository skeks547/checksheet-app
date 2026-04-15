[app]
title = CheckSheet
package.name = checksheetapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,xlsx,json
version = 1.1

# 필수 라이브러리 및 종속성 보강
requirements = python3,kivy,openpyxl,et_xmlfile,jdcal,pyjnius,android

orientation = portrait
fullscreen = 0

# 안드로이드 권한 설정 (MANAGE_EXTERNAL_STORAGE는 Google Play 거부 사유가 될 수 있으나 내부용으로는 유용)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Android API 레벨 설정 (33 = Android 13)
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
