# Octane
[![Build Status](https://travis-ci.com/leonard112/octane.svg?branch=main)](https://travis-ci.com/leonard112/octane)

Octane is a scripting language built from Python. Octane is currenly in it's early alpha stages, but the intent is for Octane to build on some of the key principles that languages like Python and Ruby follow. The Goal is for Octane to have a simple and easy to read and understand syntax.

* __[Release Notes](https://github.com/leonard112/octane/blob/main/RELEASE_NOTES.md)__

* __[Source Code](https://github.com/leonard112/octane)__

* __[Binaries](https://sourceforge.net/projects/octane-lang/files/alpha/linux/)__ _(Linux (x86) only)_
  
## Installation

* __Linux (x86):__
  * Download binaries from sourceforge.net.
    * `$ wget https://pilotfiber.dl.sourceforge.net/project/octane-lang/alpha/linux/<file name>.tgz`
  * Create a dedicated folder for the binaries to live.
    * `$ sudo mkdir /opt/octane`
  * Extract the contents ot the tar file to the folder where you want the binaries to live.
    * `$ sudo tar -xzvf <file name> --directory /opt/octane/`
  * Append the following line to `.bashrc`.
    * `$ PATH=/opt/octane:$PATH`
  * Smoke test.
    * `octane --version`

> _Before Installing Octane on __Windows__, ensure that you have __Python__ installed and __Pip__ package manager installed before you begin. Also ensure that you are running cmd or Powershell as __Administrator__._

> _Note that currently, Octane has to be built on Windows from __source__._

* __Windows:__
  * Clone this repository.
    * `> git clone https://github.com/leonard112/octane.git`
  * Navigate to the source code.
    * `> cd octane/src`
  * Install dependencies.
    * `> pip install -r requirements.txt`
  * Build octane.exe
    * `> pyinstaller --onefile  --name octane  main.py`
  * Copy everything in the `octane.exe` to your `Program Files (x86)` folder.
    * `> mkdir "C:\Program Files (x86)\Octane"`
    * `cp -r dist/octane.exe "C:\Program Files (x86)\Octane\"`
  * Append Octane to `PATH`.
    * https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
  * Smoke test.
    * `octane --version`
