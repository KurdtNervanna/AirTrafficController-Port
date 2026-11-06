Air Traffic Controller 5.03 (Walter J. Biess, 1993) running natively on Windows, macOS and Linux. The game's original 68k code runs unchanged; the parts of the classic Mac OS it uses are reimplemented.

**Downloads**

| System | File |
|---|---|
| Windows 10 or 11 (64-bit) | `ATC-Windows-x64.exe` (or the `.zip` with the manual) |
| macOS 10.13+ (Apple silicon and Intel) | `ATC-macOS-universal.dmg` or `.zip` |
| Linux x86_64 | `ATC-Linux-x86_64.AppImage` or `ATC-Linux-x86_64.tar.gz` |

**New in 1.2.0: one file, nothing to set up.** The game is now built into the program, so each download runs on its own: no game files, no folder to pick. The Windows program is a single `.exe` with no runtime libraries to install. The freeware game is included under its author's terms, which ask that it is passed on free of charge with its manual: the manual is in each package, and the program also writes a copy into its save folder.

**macOS:** the app is not notarized. The first time, right-click it and choose Open (or run `xattr -dr com.apple.quarantine "/Applications/Air Traffic Controller.app"`).

**Linux:** opening and saving schedules uses `zenity` or `kdialog`.

**Licence:** the port and its fonts are MIT-licensed (see LICENSE); the game keeps its author's freeware terms and Apple's fonts are not included (see THIRD_PARTY_NOTICES.md).
