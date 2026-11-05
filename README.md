# Air Traffic Controller 5.03 for Windows, macOS and Linux

A native port of **Air Traffic Controller 5.03** (Walter J. Biess, 1993), the
freeware successor of *Near Miss*. The game's original 68k code runs unchanged on an
embedded CPU core ([Musashi](https://github.com/kstenerud/Musashi)), and every Mac
Toolbox call it makes is answered by a small C reimplementation of the parts of the
classic Mac OS it uses. The result looks, sounds and plays like the 1993 game, in a
resizable window.

Downloads are on the [Releases](../../releases) page: a Windows zip, a universal
macOS app (Apple silicon and Intel) and a Linux AppImage or tarball.

## Game files

The port contains no game data. You need:

| File | What it is |
|---|---|
| The game | the *Air Traffic Controller 5.03* application's resource fork |
| A System file | a System 6 *System* file (only its fonts are used: Chicago, Geneva, Monaco) |

Each can be a raw resource fork, an AppleDouble file (what `unar -k visible` writes
when unpacking the original `.sit`) or a MacBinary file (what `hcopy -m` writes from a
disk image). Names don't matter; the game recognises them by their contents
(`ATC.rsrc` and `System.rsrc` are simply tried first).

Put both in a folder and start the game: on first launch it asks for that folder and
remembers it. It also looks in a `game` folder next to the program, in
`<user data folder>/game`, or in a folder given on the command line.

`tools/rfork.py extract <in> <out>` turns any of the three formats into a raw fork.

## Playing

* Mouse: as on the Mac. Click a schedule line or an aircraft, then a command button.
* **Command** is Ctrl on Windows and Linux and ⌘ on macOS (Command-N new shift);
  **Option** is Alt/Option.
* The window can be resized; the picture is scaled by whole pixels.
  `ATC_SCALE=3` sets the starting size.
* Settings, high scores and saved schedules are kept in a `save` folder: next to the
  `game` folder on Windows (or `%APPDATA%\Air Traffic Controller\save` if that isn't
  writable), `~/Library/Application Support/Air Traffic Controller/save` on macOS and
  `~/.local/share/air-traffic-controller/save` on Linux.
* Printing is reported as unavailable. On Linux, opening and saving schedules uses
  `zenity` or `kdialog`.
* macOS: the app is not notarized; the first time, right-click it and choose Open.

## Building

| Platform | How |
|---|---|
| Windows | `build.bat` (development build with a console for logs), or CMake with Visual Studio |
| macOS | `cmake -S . -B b -DCMAKE_BUILD_TYPE=Release && cmake --build b` → `Air Traffic Controller.app` |
| Linux | install the X11/Wayland/ALSA/Pulse development packages SDL needs, then the same CMake commands → `b/atc` |

On macOS and Linux CMake downloads SDL2 and links it statically
(`-DATC_FETCH_SDL=OFF` uses an installed SDL2 instead). Pushing a `v*` tag runs
`.github/workflows/release.yml`, which builds all three packages and publishes a release.

## How it works

| Source | Job |
|---|---|
| `src/trap.c` | A-line trap dispatch, 68k callbacks, Memory/OS utility traps |
| `src/mem.c` | Emulated 16 MB RAM and the Memory Manager (handles, pointers) |
| `src/rsrc.c` | Resource Manager over resource-fork files, with a settings overlay |
| `src/qd.c`, `rgn.c`, `font.c` | 1-bit QuickDraw: ports, shapes, regions, text in the real System 6 bitmap fonts, CopyBits, PICT playback |
| `src/wm.c` | Window Manager; standard frames drawn natively, the game's own round-window WDEF runs as 68k code |
| `src/menu.c`, `dlg.c`, `ctl.c` | Menu bar and menus, dialogs/alerts, buttons and scroll bars |
| `src/evt.c` | Event Manager (activate, mouse, keyboard, update events) |
| `src/fs.c`, `pack.c` | File Manager on a host folder, Standard File via native dialogs, SANE, sound |
| `src/plat.c` | Portability layer (file system, user folders) |
| `src/host_win.c`, `audio_win.c` | Windows: window, input, cursors, icon, dialogs, waveOut audio |
| `src/host_sdl.c` | macOS and Linux: the same on SDL2 |

Debug switches (environment variables): `ATC_TRACE` (every trap), `ATC_PCLOG=n,count`
(instructions after trap n), `ATC_WINLOG`, `ATC_EVLOG`, `ATC_TEXTLOG`, `ATC_CBLOG`,
`ATC_SEGLOG`, `ATC_COMPLOG`, `ATC_NOSOUND`, `ATC_WAVDUMP=file.wav` (Windows),
`ATC_HIDDEN`, `ATC_GAME=<folder>`, `ATC_SAVE=<folder>`, and
`ATC_SCRIPT="ms:action;..."` for headless runs (`click x y`, `down/move/up x y`,
`key c`, `cmd c`, `dump file.pbm`, `quit`). `tools/pbm2png.py` converts screen dumps.

## Credits

*Air Traffic Controller* © 1986–1993 Walter J. Biess. Musashi © Karl Stenerud (MIT
licence, see `musashi/readme.txt`). Port code by KurdtNervanna.
