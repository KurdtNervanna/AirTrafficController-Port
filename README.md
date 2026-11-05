# Air Traffic Controller 5.03 — for Windows, macOS and Linux

[![Release](https://img.shields.io/github/v/release/KurdtNervanna/AirTrafficController-Port)](../../releases/latest)
![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20macOS%20%7C%20Linux-blue)
[![Build](https://github.com/KurdtNervanna/AirTrafficController-Port/actions/workflows/release.yml/badge.svg)](../../actions/workflows/release.yml)

A native port of **Air Traffic Controller 5.03**, Walter J. Biess's classic Macintosh
air traffic control simulator (1986–1993) and the freeware successor of *Near Miss*.

The game is not rewritten or re-imagined: its **original 68k code runs unchanged** on an
embedded CPU core, and every call it makes into the classic Mac OS — windows, menus,
dialogs, QuickDraw graphics, fonts, files, sound — is answered by a compact C
reimplementation of those parts of the Mac Toolbox. It looks, sounds and plays exactly
like it did on a 1993 Macintosh, in a resizable window on a modern computer.

![Air Traffic Controller running: radar screen with aircraft, airports, hills, towers and a restricted zone; the air traffic schedule with one jet selected; and the control command panel](docs/screenshots/gameplay.png)

## Contents

- [Download](#download)
- [Getting the game files](#getting-the-game-files)
- [How to play](#how-to-play)
- [Screenshots](#screenshots)
- [What works](#what-works)
- [Building from source](#building-from-source)
- [How it works](#how-it-works)
- [Credits and legal](#credits-and-legal)

## Download

Get the latest build from the [Releases](../../releases/latest) page.

| System | File | First run |
|---|---|---|
| **Windows** 10/11 (x64) | `ATC-Windows-x64.zip` | Unzip anywhere and run `ATC.exe`. |
| **macOS** 10.13 or later, Apple silicon and Intel | `ATC-macOS-universal.dmg` | Drag *Air Traffic Controller* to Applications. The app is not notarized, so the first time **right-click it and choose Open** (or run `xattr -dr com.apple.quarantine "/Applications/Air Traffic Controller.app"`). |
| **Linux** x86_64 | `ATC-Linux-x86_64.AppImage` or `ATC-Linux-x86_64.tar.gz` | `chmod +x ATC-Linux-x86_64.AppImage` and run it, or unpack the tarball and run `./atc`. Opening and saving schedules uses `zenity` or `kdialog`. |

**The downloads do not contain the game itself** — see the next section. On first launch
the program asks for the folder that holds the game files and remembers it.

## Getting the game files

You need two files from the classic Mac world:

| File | Where it comes from |
|---|---|
| **Air Traffic Controller 5.03** | The application itself. It was released as freeware in 1992–93 and is available from classic Macintosh software archives (it is usually distributed as `Air Traffic Controller 5.03.sit`). |
| **A System 6 System file** | The *System* file from any System 6 installation (6.0.x). Only its bitmap fonts — Chicago, Geneva and Monaco — are used, so text looks exactly as it did. |

Classic Mac files keep their contents in a *resource fork*, which modern systems don't
store natively. Any of these three forms works, and the names don't matter — the program
recognises each file by its contents:

* a **MacBinary** file (`.bin`),
* an **AppleDouble** file (the `._name` or `name.rsrc` companion that unpacking tools write),
* a **raw resource fork** (for example `ATC.rsrc`).

**From the original `.sit` archive** (with [The Unarchiver](https://theunarchiver.com/)'s
command-line tool):

```sh
unar -k visible "Air Traffic Controller 5.03.sit"
# -> "Air Traffic Controller 5.03/Air Traffic Controller 5.03.rsrc"  (AppleDouble: use it as is)
```

**A System file from a disk image** (with [hfsutils](https://www.mars.org/home/rob/proj/hfs/)):

```sh
hmount "System Tools.dsk"
hcd "System Folder"
hcopy -m System System.bin          # MacBinary: use it as is
humount
```

From an emulator such as Mini vMac or Basilisk II you can also export both files as
MacBinary. `tools/rfork.py extract <in> <out>` converts any of the forms to a raw fork.

Put both files in one folder and start the game. It looks, in order, in a folder named on
the command line, in `$ATC_GAME`, in a `game` folder next to the program, in
`<user data folder>/game`, and in the folder you picked last time.

## How to play

You are in charge of all the air traffic in your sector for one shift. Every aircraft on
the **schedule** must leave through its assigned exit — a compass point at a set altitude,
or an airport — before its fuel runs out, without coming too close to other aircraft.
Aircraft move once per **turn** (15 seconds): jets every turn, propeller planes every
second turn, helicopters every fourth.

1. **Start a shift** with *Simulate ▸ With New Schedule* (Command-N).
2. **Select an aircraft**: click it on the radar, or click its line in the schedule.
3. **Give it a command** from the *Aircraft Control Commands* panel:
   * **Turns** of 45°, 90°, 135° or 180° left or right; **Δ** flies straight on; **∞**
     circles (only while already turning).
   * **Altitude** levels **0–8**; aircraft climb or descend one level per move. **L**
     lands at the destination airport when the path crosses it (only at or bound for
     level 1). Aircraft waiting at an airport (**Δ** on the schedule) take off when given
     an altitude.
4. Watch for **near misses** (aircraft too close in altitude and distance, or flying through
   the restricted zone) and **thunderstorms** — both cost points. Collisions, hitting hills
   or towers, running out of fuel or landing from the wrong direction end in a crash.

The schedule's columns show the aircraft type (**J**et, **P**rop, **H**elicopter),
current heading and altitude, commanded heading and altitude, entry and exit points, fuel
time and entry time. Click the **Pause** box to stop the clock; click the **turn timer**
(the small circle) or the **shift clock** to skip ahead one turn. Holding the mouse
button on the edge of the radar previews aircraft about to enter there.
*Options ▸ Set Simulation Options* sets the number of aircraft, shift length, airports,
separation, obstacles, restricted zone and weather; the full manual comes with the game.

### Keyboard

**Command** is **Ctrl** on Windows and Linux and **⌘** on macOS. **Option** is **Alt/Option**.

| Keys | Menu command |
|---|---|
| Command-N / Command-C | Simulate with a new / the current schedule |
| Command-E | End simulation |
| Command-L / Command-S | Load / save schedule |
| Command-O | Set simulation options |
| Command-H | Show high scores |
| Command-P | Play back the last simulation |
| Command-B / Command-R | Conflict blinking / radar sweep on or off |
| Command-W | Sound effects |
| Command-G / Command-F | Faster / fastest (any click or key returns to normal speed) |
| Command-A | About |
| Command-Q | Quit |

### Window and saved data

* The window can be resized freely; the picture is scaled by whole pixels so it stays sharp.
  Set `ATC_SCALE=3` (or any number) to choose the starting size.
* Settings, high scores and saved schedules are kept in a `save` folder:

  | System | Location |
  |---|---|
  | Windows | next to the game folder; if that isn't writable, `%APPDATA%\Air Traffic Controller\save` |
  | macOS | `~/Library/Application Support/Air Traffic Controller/save` |
  | Linux | `~/.local/share/air-traffic-controller/save` (or under `$XDG_DATA_HOME`) |

## Screenshots

| | |
|---|---|
| ![Title screen: AIR TRAFFIC CONTROLLER Version 5.03, an airliner and the radar](docs/screenshots/title.png) | ![The Options menu pulled down over the radar](docs/screenshots/menus.png) |
| *Title screen* | *Menus, with their original keyboard shortcuts* |
| ![Simulator Options dialog with radio buttons for aircraft, minutes, airports, spacing, obstacles, restricted zone and weather](docs/screenshots/options.png) | ![High Scores dialog](docs/screenshots/high-scores.png) |
| *Simulation options* | *High scores* |
| ![About box with the distribution terms](docs/screenshots/about.png) | ![The game in a Windows 11 window](docs/screenshots/windows-window.png) |
| *About box* | *Running in a Windows window* |

## What works

Everything a player touches: the title screen; starting, playing and ending shifts;
selecting aircraft on the radar or schedule; all turn, altitude, landing and circling
commands; the radar sweep and conflict blinking; weather, hills, towers and restricted
zones; the schedule with its scroll bar; the shift clock, wind, score and turn timer;
pause and skip-a-turn; simulation options; high scores (saved); the
About box; sound effects; and loading and saving schedules through the system's own file
dialogs.

Known limitations:

* **Black and white.** The game is told it is running on a Mac without Color QuickDraw,
  so the *Set Icon Colors* and *Set Text Options* (large-screen) menu items don't appear —
  exactly as on a compact Mac.
* **Printing** (*Print Display / Poster / Schedule*) is reported as unavailable.
* **Near Miss 1.0**, the earlier commercial version, spoke its messages through MacinTalk;
  that version isn't supported (5.03 has no speech).

## Building from source

| System | Requirements | Build |
|---|---|---|
| Windows | Visual Studio 2019/2022 or the Build Tools ("Desktop development with C++") | `build.bat` (development build with a console for logs), or `cmake -S . -B b -A x64 && cmake --build b --config Release` |
| macOS | Xcode command-line tools, CMake | `cmake -S . -B b -DCMAKE_BUILD_TYPE=Release && cmake --build b` → `b/Air Traffic Controller.app` |
| Linux | gcc or clang, CMake, and the X11/Wayland/ALSA/PulseAudio development packages SDL needs | the same commands → `b/atc` |

On macOS and Linux CMake downloads SDL2 and links it statically, so the result has no
SDL dependency; `-DATC_FETCH_SDL=OFF` uses an installed SDL2 instead. For a universal
macOS build add `-DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"`.

Releases are built by [`.github/workflows/release.yml`](.github/workflows/release.yml):
pushing a `v*` tag builds all three packages and publishes them as a GitHub release
(running the workflow by hand builds them as artifacts only).

## How it works

The game is a Lightspeed Pascal application in 15 code segments. The port loads them,
builds the A5 world and jump table exactly as the Mac's Segment Loader did, and runs the
code on [Musashi](https://github.com/kstenerud/Musashi) as a 68020. Every Toolbox or OS
call is an A-line trap: the CPU core hands it to the dispatcher, which implements it in C
on top of an emulated 16 MB address space — where windows, menus, regions, handles and
QuickDraw ports live in their real Mac layouts, because the game reads and writes their
fields directly.

| Source | Job |
|---|---|
| `src/trap.c` | A-line trap dispatch, calls back into 68k code, Memory Manager and OS utility traps |
| `src/mem.c` | Emulated RAM and the Memory Manager (handles and pointers) |
| `src/rsrc.c` | Resource Manager over resource-fork files, with a settings overlay for what the game writes back |
| `src/qd.c`, `rgn.c`, `font.c` | 1-bit QuickDraw: ports, pens, patterns, shapes, true regions, text in the System 6 bitmap fonts, CopyBits and PICT playback |
| `src/wm.c` | Window Manager with real visible regions and update events; standard frames drawn natively, the game's own round-window definition (WDEF) runs as 68k code |
| `src/menu.c`, `dlg.c`, `ctl.c` | Menu bar and menus, dialogs and alerts, buttons, check boxes, radio buttons and scroll bars |
| `src/evt.c` | Event Manager (activate, mouse, keyboard and update events) |
| `src/fs.c`, `pack.c` | File Manager over a host folder, Standard File through native dialogs, SANE, the Sound Manager and Sound Driver |
| `src/plat.c` | Portability layer (files, folders, user data locations) |
| `src/host_win.c`, `audio_win.c` | Windows host: window, input, cursors, icon, dialogs and waveOut audio |
| `src/host_sdl.c` | macOS and Linux host on SDL2 |
| `tools/` | Resource-fork extraction, a 68k disassembler and trap audit for the game, screenshot conversion, the icon generator |

### Debugging

Environment variables switch on logging and testing aids:

| Variable | Effect |
|---|---|
| `ATC_TRACE=1` | log every trap |
| `ATC_PCLOG=n,count` | log `count` instructions after trap number `n` |
| `ATC_WINLOG`, `ATC_EVLOG`, `ATC_TEXTLOG`, `ATC_CBLOG`, `ATC_SEGLOG`, `ATC_COMPLOG` | log windows, events, text drawing, CopyBits, segment loading, window composition |
| `ATC_GAME=<folder>`, `ATC_SAVE=<folder>` | game and save folders |
| `ATC_NOSOUND=1`, `ATC_WAVDUMP=file.wav` | no sound / record the sound output (Windows) |
| `ATC_HIDDEN=1` | run without showing the window |
| `ATC_SCRIPT="ms:action;..."` | scripted input for headless tests: `click x y`, `down x y`, `move x y`, `up x y`, `key c`, `cmd c`, `dump file.pbm`, `quit` |

`tools/pbm2png.py` converts the `dump` screenshots to PNG.

## Credits and legal

* **Air Traffic Controller** © 1986–1993 Walter J. Biess. Released as freeware; its own
  terms allow free distribution together with its manual. This project does not include
  the game and is not affiliated with its author.
* **Macintosh system fonts** © Apple. They are not included; the program reads them from
  a System file you provide.
* **Musashi** 68000 core © 1998–2002 Karl Stenerud, MIT licence (see `musashi/readme.txt`).
  It includes SoftFloat by John R. Hauser (see `musashi/softfloat/README.txt`).
* Port by **KurdtNervanna**.
