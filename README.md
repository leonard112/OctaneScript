# OctaneScript [![Build Status](https://travis-ci.com/leonard112/octane.svg?branch=main)](https://travis-ci.com/leonard112/octanescript)

<img src="https://github.com/leonard112/octane/blob/main/images/octanescript-logo.svg" alt="OctaneScript Logo" width=25%></img>

OctaneScript is a scripting language built from Python. OctaneScript is currenly in it's early alpha stages, but the intent is for OctaneScript to build on some of the key principles that languages like Python and Ruby follow. The Goal is for Octane to have a simple and easy to read and understand syntax. 

Note that this language is not being developed for any customer or particular use. I am simply creating this language for fun. Feel free to do whatever you want with this software. See [MIT License](LICENSE)

Feel free to open and issue if you find any bugs or if you have any feature suggestions

* __[Source Code](https://github.com/leonard112/OctaneScript)__

* __[Binaries](https://sourceforge.net/projects/octanescript/files/alpha/linux/amd64/dev)__ _(Linux (amd64) only)_
  
## Installation

### Linux
* __Debian:__
  * Download Debian package from sourceforge.net.
    * `$ wget https://pilotfiber.dl.sourceforge.net/project/octanescript/alpha/linux/amd64/dev/octanescript-<version>.tgz`
  * Install package.
    * `$ sudo dpkg -i octanescript-<version>`
* __Tar:__
  * Download binaries from sourceforge.net.
    * `$ wget https://pilotfiber.dl.sourceforge.net/project/octanescript/alpha/linux/amd64/dev/octanescript-<version>.tgz`
  * Create a dedicated folder for the binaries to live.
    * `$ sudo mkdir /opt/octanescript`
  * Extract the contents ot the tar file to the folder where you want the binaries to live.
    * `$ sudo tar -xzvf <file name> --directory /opt/octanescript/`
  * Append the following line to `.bashrc`.
    * `$ PATH=/opt/octanescript:$PATH`
  * Smoke test.
    * `os --version`

> _Before Installing Octane on __Windows__, ensure that you have __Python__ installed and __Pip__ package manager installed before you begin. Also ensure that you are running cmd or Powershell as __Administrator__._

> _Note that currently, Octane has to be built on Windows from __source__._

* __Windows:__
  * Clone this repository.
    * `> git clone https://github.com/leonard112/OctaneScript.git`
  * Navigate to the source code.
    * `> cd OctaneScript/src`
  * Install dependencies.
    * `> pip install -r requirements.txt`
  * Build os.exe
    * `> pyinstaller --onefile  --name os  main.py`
  * Copy everything in the `octane.exe` to your `Program Files (x86)` folder.
    * `> mkdir "C:\Program Files (x86)\OctaneScript"`
    * `cp -r dist/os.exe "C:\Program Files (x86)\OctaneScript\"`
  * Append OctaneScript to `PATH`.
    * https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
  * Smoke test.
    * `os --version`
