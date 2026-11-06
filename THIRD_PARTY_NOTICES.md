# Licences and notices

The MIT licence in [LICENSE](LICENSE) covers the code of this port and its built-in
fonts (Tower 12, Radar 9 and Radar 12 in `fonts/`, drawn from scratch for this project):
everything in this repository except the components below, which keep their own terms.

## Air Traffic Controller (included: `data/`)

**Air Traffic Controller 5.03** © 1986–1993 Walter J. Biess. The application's resource
fork (`data/ATC.rsrc`) and its manual (`data/Manual.txt`, converted from the original
TeachText file) are included and compiled into every build. This project is not
affiliated with the author, and the MIT licence does not apply to them: they are passed
on under the game's own freeware terms, from its About box:

> This program and its manual may be distributed together by:
> 1) Individuals as long as no fee is charged for the program;
> 2) Apple Users Groups as long as no fee is charged for the program except that a
>    nominal disk copying fee may be charged;
> 3) Electronic information services and bulletin boards as long as no charge is made
>    for the program except for the normal connect time charge.
>
> Without the written consent of the author, other methods of distribution are
> prohibited. This program may not be included in collections of public domain/shareware
> programs that are sold on floppies, CD-ROM or other media.

So the game must be passed on free of charge and with its manual: every package of this
project includes the manual, and the program also writes it into its save folder the
first time it runs.

## Not included: the Macintosh fonts

**Macintosh system fonts** (Chicago, Geneva, Monaco) © Apple. They are not included. If
the player supplies a System file, the program reads them from it at run time; otherwise
it uses its own built-in fonts. Only the fonts' advance widths and line metrics were
matched, so that text lays out the same; the glyphs are original.

The screenshots in `docs/screenshots` show the game running in this port, for
illustration.

## Included in the source and the builds

### Musashi (`musashi/`)

Motorola 680x0 emulator. Copyright © 1998–2002 Karl Stenerud. MIT licence; the full
text is in [`musashi/readme.txt`](musashi/readme.txt).

### SoftFloat (`musashi/softfloat/`)

IEC/IEEE floating-point arithmetic package, release 2b, by John R. Hauser, as
repackaged for MAME. Its legal notice, from
[`musashi/softfloat/README.txt`](musashi/softfloat/README.txt):

> SoftFloat was written by me, John R. Hauser. This work was made possible in part by
> the International Computer Science Institute, located at Suite 600, 1947 Center
> Street, Berkeley, California 94704. Funding was partially provided by the National
> Science Foundation under grant MIP-9311980. The original version of this code was
> written as part of a project to build a fixed-point vector processor in
> collaboration with the University of California at Berkeley, overseen by Profs.
> Nelson Morgan and John Wawrzynek.
>
> THIS SOFTWARE IS DISTRIBUTED AS IS, FOR FREE. Although reasonable effort has been
> made to avoid it, THIS SOFTWARE MAY CONTAIN FAULTS THAT WILL AT TIMES RESULT IN
> INCORRECT BEHAVIOR. USE OF THIS SOFTWARE IS RESTRICTED TO PERSONS AND ORGANIZATIONS
> WHO CAN AND WILL TAKE FULL RESPONSIBILITY FOR ALL LOSSES, COSTS, OR OTHER PROBLEMS
> THEY INCUR DUE TO THE SOFTWARE, AND WHO FURTHERMORE EFFECTIVELY INDEMNIFY JOHN HAUSER
> AND THE INTERNATIONAL COMPUTER SCIENCE INSTITUTE (possibly via similar legal warning)
> AGAINST ALL LOSSES, COSTS, OR OTHER PROBLEMS INCURRED BY THEIR CUSTOMERS AND CLIENTS
> DUE TO THE SOFTWARE.
>
> Derivative works are acceptable, even for commercial purposes, provided that the
> minimal documentation requirements stated in the source code are satisfied.

### SDL 2 (macOS and Linux builds only)

Simple DirectMedia Layer, downloaded at build time and linked statically into the macOS
and Linux programs. Copyright © 1997–2024 Sam Lantinga. zlib licence:

> This software is provided 'as-is', without any express or implied warranty. In no
> event will the authors be held liable for any damages arising from the use of this
> software.
>
> Permission is granted to anyone to use this software for any purpose, including
> commercial applications, and to alter it and redistribute it freely, subject to the
> following restrictions:
>
> 1. The origin of this software must not be misrepresented; you must not claim that you
>    wrote the original software. If you use this software in a product, an
>    acknowledgment in the product documentation would be appreciated but is not
>    required.
> 2. Altered source versions must be plainly marked as such, and must not be
>    misrepresented as being the original software.
> 3. This notice may not be removed or altered from any source distribution.
