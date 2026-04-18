[app]
title = Step2-5Test
package.name = checksheetstep25
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 0.6
# 검증 완료된 라이브러리 + android 패키지
requirements = python3,kivy,pyjnius,openpyxl,et_xmlfile,jdcal,pysmb,pyasn1,six,tqdm,pycryptodome,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
