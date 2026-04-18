[app]
title = Step2-6Test
package.name = checksheetstep26
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 0.7
# 모든 검증된 라이브러리 유지
requirements = python3,kivy,pyjnius,openpyxl,et_xmlfile,jdcal,pysmb,pyasn1,six,tqdm,pycryptodome,android
# [의심 포인트] pdfjs 폴더를 에셋으로 포함
android.add_assets = pdfjs
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
