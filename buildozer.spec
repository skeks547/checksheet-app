[app]
title = Step2-2TestRev
package.name = checksheetstep22rev
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 0.3.1
# openpyxl의 필수 의존성 추가
requirements = python3,kivy,pyjnius,openpyxl,et_xmlfile,jdcal
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
