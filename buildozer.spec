[app]
title = CheckSheet
package.name = checksheetapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,xlsx,json
version = 1.4

# 필수 라이브러리 (네트워크 상태 확인을 위해 ACCESS_NETWORK_STATE 추가 고려)
requirements = python3,kivy,openpyxl,et_xmlfile,jdcal,pyjnius,android,pysmb,pyasn1

orientation = portrait
fullscreen = 0

# 권한 설정 (ACCESS_NETWORK_STATE 추가)
android.permissions = INTERNET, ACCESS_NETWORK_STATE, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Android API 레벨 설정
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
