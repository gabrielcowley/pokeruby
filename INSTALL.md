# Prerequisites

| Linux | macOS | Windows 10 (build 18917+) | Windows 10 (1709+) | Windows Vista, 7, 8, 8.1, and 10 (1507, 1511, 1607, and 1703)
| ----- | ----- | ------------------------- | ------------------ | ---------------------------------------------------------
| none | [Xcode Command Line Tools package][xcode] | [Windows Subsystem for Linux 2][wsl2] | [Windows Subsystem for Linux][wsl] | MSYS2 (see below)

[xcode]: https://developer.apple.com/library/archive/technotes/tn2339/_index.html#//apple_ref/doc/uid/DTS40014588-CH1-DOWNLOADING_COMMAND_LINE_TOOLS_IS_NOT_AVAILABLE_IN_XCODE_FOR_MACOS_10_9__HOW_CAN_I_INSTALL_THEM_ON_MY_MACHINE_
[wsl2]: https://docs.microsoft.com/windows/wsl/wsl2-install
[wsl]: https://docs.microsoft.com/windows/wsl/install-win10

The [prerelease version of the Linux subsystem](https://docs.microsoft.com/windows/wsl/install-legacy) available in the 1607 and 1703 releases of Windows 10 is obsolete so consider uninstalling it.

Make sure that the `build-essential`, `binutils-arm-none-eabi`, `git`, and `libpng-dev` packages are installed. The `build-essential` package includes the `make`, `gcc-core`, and `g++` packages so they do not have to be obtained separately. MSYS2 does not include `libpng-dev` so it must be built from source.

On Linux and Mac OS X, using `(dkp-)pacman`, install `gba-dev`. This will give you devkitARM and all its extensions.

Install the **devkitARM** toolchain of [devkitPro](https://devkitpro.org/wiki/Getting_Started) and add its environment variables. For Windows versions without the Linux subsystem, the devkitPro [graphical installer](https://github.com/devkitPro/installer/releases) includes a preconfigured MSYS2 environment, thus the steps below are not required.

	export DEVKITPRO=/opt/devkitpro
	echo "export DEVKITPRO=$DEVKITPRO" >> ~/.bashrc
	export DEVKITARM=$DEVKITPRO/devkitARM
	echo "export DEVKITARM=$DEVKITARM" >> ~/.bashrc
	
Refer to [this guide](https://www.pokecommunity.com/showthread.php?t=432351) for a step-by-step version of these instructions.

### Platform-specific notes
#### Mac OS X
It is highly recommended that you use the [Homebrew](https://brew.sh) package manager. Suggested packages include `gcc`, `libpng`, `coreutils`, `git`, `make`, and `md5sha1sum`. Note that `make` will be aliased as `gmake` in Terminal, and `gcc` as `gcc-${VM}` where `${VM}` is the GCC major version (currently 9).

If you have installed `libpng` via Homebrew and you're using an ARM-based system, you need to append `-I /opt/homebrew/include/ -L /opt/homebrew/lib/` to the `CFLAGS` or `CXXFLAGS` assignments in the Makefiles for `rsfont`, `preproc` and `gbagfx`.

# Installation

To set up the repository:

	git clone https://github.com/pret/pokeruby
	git clone https://github.com/pret/agbcc

	cd ./agbcc
	./build.sh
	./install.sh ../pokeruby

	cd ../pokeruby

Also, obtain the `poryscript` executable and `font_config.json` from https://github.com/huderlem/poryscript/releases and copy them to `tools/poryscript`. The version used at time of writing is `3.0.1`.

To build Pokémon Ruby:

	make ruby

To build Pokémon Sapphire:

    make sapphire

The above two commands will build the English v1.0 version of the respective title. To build the 1.1 and 1.2 revisions, use the appropriate `_rev` target. For example, to build Ruby 1.2, run:

    make ruby_rev2

To also build debug targets (only v1.0 is currently supported), run either of the following:

    make ruby_debug
    make sapphire_debug

To compare between official ROM images for each target:

    make (target) COMPARE=1

## Notes

* If the base tools are not found on macOS in new Terminal sessions after the first successful build, run `echo "if [ -f ~/.bashrc ]; then . ~/.bashrc; fi" >> ~/.bash_profile` once to prevent the issue from occurring again. Verify that the `devkitarm-rules` package is installed as well; if not, install it by running `sudo dkp-pacman -S devkitarm-rules`.

* If the repository was previously set up using Cygwin, delete the `.exe` files in the subfolders of the `tools` folder except for `agbcc` and try building again. [Learn the differences between MSYS2 and Cygwin.](https://github.com/msys2/msys2/wiki/How-does-MSYS2-differ-from-Cygwin)

## Notes about the German language ROMs
This repository also supports the "first edition" German versions of Ruby and Sapphire. However, due to major differences in scripts, text, and graphics, a special configuration needs to be set up before compilation and torn down after.

To set up the repository:

    make clean
    sh de_before.sh

To compile the "first edition" German ROMs:

    make ruby_de
    make sapphire_de

To compile their debug equivalents:

    make ruby_de_debug
    make sapphire_de_debug

To restore the repository (**MUST BE DONE BEFORE ATTEMPTING TO BUILD ANY ENGLISH LANGUAGE ROM**):

    make clean
    sh de_after.sh

## Parallel builds

See [the GNU docs](https://www.gnu.org/software/make/manual/html_node/Parallel.html) and [this Stack Exchange thread](https://unix.stackexchange.com/questions/208568) for more information.

To speed up building, run:

	make -j$(nproc)

`nproc` is not available on macOS. The alternative is `sysctl -n hw.ncpu` ([relevant Stack Overflow thread](https://stackoverflow.com/questions/1715580)).

## Building without dependency scanning

If only `.c` or `.s` files were changed, turn off the dependency scanning temporarily. Changes to any other files will be ignored and the build will either fail or not reflect those changes.

	make NODEP=1

## Building with devkitARM's C compiler

This project supports the `arm-none-eabi-gcc` compiler included with devkitARM. To build this target, simply run:

	make modern

## Building with other toolchains

To build using a toolchain other than devkitARM, override the `TOOLCHAIN` environment variable with the path to your toolchain, which must contain the subdirectory `bin`.

	make TOOLCHAIN="/path/to/toolchain/here"

The following is an example:

	make TOOLCHAIN="/usr/local/arm-none-eabi"

To compile the `modern` target with this toolchain, the subdirectories `lib`, `include`, and `arm-none-eabi` must also be present.

## Building with debug info

To build **pokeruby.elf** with enhanced debug info, use the `DINFO` variable.

	make DINFO=1
