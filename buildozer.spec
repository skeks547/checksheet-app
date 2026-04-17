[app]
title = CheckSheetFinal
package.name = checksheetv30
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,pdf,xlsx,json,html,js,css,map
source.exclude_dirs = backup, bin, .buildozer
# [핵심] pdfjs 폴더를 앱 에셋으로 통째로 포함
android.add_assets = pdfjs
version = 3.0

requirements = python3,kivy,pyjnius,android,openpyxl,pysmb,pyasn1,six,tqdm,et_xmlfile,jdcal,pycryptodome

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# WebView 기반이므로 특수 라이브러리 의존성 없음
android.gradle_dependencies = 
android.enable_androidx = True
android.enable_jetifier = True

android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
