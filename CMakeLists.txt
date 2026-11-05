cmake_minimum_required(VERSION 3.16)
project(AirTrafficController C)

set(CMAKE_C_STANDARD 99)
if(EXISTS ${CMAKE_SOURCE_DIR}/VERSION)
  file(STRINGS ${CMAKE_SOURCE_DIR}/VERSION ATC_VERSION LIMIT_COUNT 1)
else()
  set(ATC_VERSION dev)
endif()

set(ATC_CORE
  src/main.c src/trap.c src/mem.c src/rsrc.c src/qd.c src/rgn.c src/font.c src/wm.c
  src/menu.c src/ctl.c src/dlg.c src/evt.c src/fs.c src/pack.c src/plat.c src/fonts_builtin.c
  musashi/m68kcpu.c musashi/m68kops.c musashi/m68kdasm.c musashi/softfloat/softfloat.c)

if(WIN32)
  add_executable(ATC WIN32 ${ATC_CORE} src/host_win.c src/audio_win.c platform/windows/atc.rc)
  target_link_libraries(ATC user32 gdi32 winmm comdlg32 shell32 ole32)
  if(MSVC)
    target_compile_definitions(ATC PRIVATE _CRT_SECURE_NO_WARNINGS)
    target_link_options(ATC PRIVATE /ENTRY:mainCRTStartup)
  endif()
else()
  # SDL2, built statically from source by default so the game has no runtime dependency on it
  option(ATC_FETCH_SDL "Build SDL2 from source and link it statically" ON)
  if(ATC_FETCH_SDL)
    include(FetchContent)
    set(SDL_SHARED OFF CACHE BOOL "" FORCE)
    set(SDL_STATIC ON CACHE BOOL "" FORCE)
    set(SDL_TEST OFF CACHE BOOL "" FORCE)
    FetchContent_Declare(SDL2 URL https://github.com/libsdl-org/SDL/releases/download/release-2.30.9/SDL2-2.30.9.tar.gz)
    FetchContent_MakeAvailable(SDL2)
    set(ATC_SDL SDL2::SDL2-static)
  else()
    find_package(SDL2 REQUIRED)
    set(ATC_SDL SDL2::SDL2)
  endif()
  if(APPLE)
    add_executable(ATC MACOSX_BUNDLE ${ATC_CORE} src/host_sdl.c)
    set_target_properties(ATC PROPERTIES
      OUTPUT_NAME "Air Traffic Controller"
      MACOSX_BUNDLE_INFO_PLIST ${CMAKE_SOURCE_DIR}/platform/macos/Info.plist.in
      MACOSX_BUNDLE_BUNDLE_NAME "Air Traffic Controller"
      MACOSX_BUNDLE_GUI_IDENTIFIER "com.kurdtnervanna.atc"
      MACOSX_BUNDLE_BUNDLE_VERSION ${ATC_VERSION}
      MACOSX_BUNDLE_SHORT_VERSION_STRING ${ATC_VERSION}
      MACOSX_BUNDLE_ICON_FILE atc.icns)
    set_source_files_properties(platform/macos/atc.icns PROPERTIES MACOSX_PACKAGE_LOCATION Resources)
    target_sources(ATC PRIVATE platform/macos/atc.icns)
  else()
    add_executable(ATC ${ATC_CORE} src/host_sdl.c)
    set_target_properties(ATC PROPERTIES OUTPUT_NAME "atc")
  endif()
  target_link_libraries(ATC ${ATC_SDL} m)
  target_compile_options(ATC PRIVATE -Wno-unused-result -Wno-format-truncation)
endif()

target_include_directories(ATC PRIVATE src musashi)
target_compile_definitions(ATC PRIVATE ATC_VERSION="${ATC_VERSION}")
