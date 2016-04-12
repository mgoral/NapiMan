NapiMan is a program which downloads Polish subtitles by a video title, length
and frames per second because searching videos by some calculated has often
fails.

# Usage

Just run `napiman` with a list of video files for which you would like to
download subtitles. NapiMan will then query NapiProjekt's (C) website and
present you a list of titles which match the name of your video. When you choose
one, NapiMan will download best matching subtitle.

There are several options which allow a more manual control over what NapiMan
searches and downloads. To learn more about them, type `napiman -h`.

# Installation

Installation is quite simple: just type `make install`. If you wish to install
in a different prefix than the default one (`$HOME/.local`), you can edit a
`config.mk` file. NapiMan also respects `$DESTDIR` environment variable, so the
full installation path is in fact `${DESTDIR}${prefix}`. You can also set
prefix when calling make: `make install prefix=/usr`.

When installing, NapiMan will create a [virtualenv][venv] and download all its
dependencies so you are required to only have a virtualenv installed and
accessible in your `$PATH`. NapiMan dependencies are listed in
[requirements.txt][reqs].

If your system has all dependencies installed (or you simply don't want create a
virtualenv), just call `make` and grab the executable from a `build` directory.
You can call it directly.

# Legal issues

This program is licensed under GPLv3 or (at your opinion) any later version of
GPL. For details see [LICENSE][license].

This program only queries NapiProjekt's database. It is not related anyhow with
NapiProjekt or NapiProjekt's authors.

  [license]: LICENSE
  [reqs]: requirements.txt
  [venv]: https://pypi.python.org/pypi/virtualenv

<!-- vim: set tw=80 : -->
