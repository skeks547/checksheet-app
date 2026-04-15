[app]
title = CheckSheet
package.name = checksheetapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,xlsx,json
version = 1.6

# 필수 라이브러리
requirements = python3,kivy,openpyxl,et_xmlfile,jdcal,pyjnius,android,pysmb,pyasn1

orientation = portrait
fullscreen = 0

# 권한 설정
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, CHANGE_WIFI_MULTICAST_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Android API 레벨
android.api = 33
android.minapi = 21

# 보안 정책 우회 (Cleartext 트래픽 허용)
android.manifest.application_attr = android:usesCleartextTraffic="true"

[buildozer]
log_level = 2
warn_on_root = 1
