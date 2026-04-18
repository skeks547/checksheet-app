[app]
title = Step2-4Test
package.name = checksheetstep24
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 0.5
# pycryptodome 추가
requirements = python3,kivy,pyjnius,openpyxl,et_xmlfile,jdcal,pysmb,pyasn1,six,tqdm,pycryptodome
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
