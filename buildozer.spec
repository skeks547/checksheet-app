[app]
title = CheckSheet
package.name = checksheetapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,xlsx,json
version = 1.0

# [수정] 최소 핵심 라이브러리 구성
requirements = python3,kivy,openpyxl,et_xmlfile,jdcal,pyjnius,android,pysmb,pyasn1,six

orientation = portrait
fullscreen = 0

# [수정] 파일 접근 및 네트워크 권한
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# [수정] 네이티브 PDF 뷰어 라이브러리 (이것이 벡터 렌더링 엔진입니다)
android.gradle_dependencies = com.github.barteksc:android-pdf-viewer:2.8.2

# [추가] 최신 라이브러리 호환성을 위한 필수 설정
android.enable_androidx = True

# Android API 레벨 설정
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
