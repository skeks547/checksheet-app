[app]
title = CheckSheet
package.name = checksheetapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,xlsx,json
version = 1.0

# [ìµœì ?? ?„ìˆ˜ ?¼ì´ë¸ŒëŸ¬ë¦?
requirements = python3,kivy,openpyxl,et_xmlfile,jdcal,pyjnius,android,pysmb,pyasn1,six

orientation = portrait
fullscreen = 0

# [ê¶Œí•œ]
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE

# [?¤ì´?°ë¸Œ PDF ?¼ì´ë¸ŒëŸ¬ë¦? - 2.8.2 ë²„ì „ ? ì?
android.gradle_dependencies = com.github.barteksc:android-pdf-viewer:3.2.0-beta.1

# [ì¤‘ìš”] AndroidX ë°?Jetifier ?œì„±??(?¬ë˜??ë°©ì? ?µì‹¬)
android.enable_androidx = True
android.gradle_options = android.useAndroidX=true, android.enableJetifier=true

# [ë¹Œë“œ ê°€??ë°?ë©”ëª¨ë¦??¤ì •] - ë¹Œë“œ ë©ˆì¶¤ ë°©ì?
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# Android API ?¤ì •
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
