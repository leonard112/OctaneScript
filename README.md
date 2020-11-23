# OctaneScript [![Build Status](https://travis-ci.com/leonard112/OctaneScript.svg?branch=main)](https://travis-ci.com/leonard112/OctaneScript) [![Download OctaneScript](https://img.shields.io/sourceforge/dt/octanescript.svg)](https://sourceforge.net/projects/octanescript/files/alpha/linux/amd64/dev/)

  <img src="https://github.com/leonard112/octane/blob/main/images/octanescript-logo.svg" alt="OctaneScript Logo" width=25%></img>

OctaneScript is a scripting language built from Python. OctaneScript is currenly in it's early alpha stages.

:warning: Note that this language is not being developed for any customer or particular use. This lanauge is being developed for fun. Feel free to use this software for whatever you wish, but ensure that you review this software's [license](https://github.com/leonard112/OctaneScript/blob/main/LICENSE) _(MIT)_ if you consider using this software for anything more exploration and learning. 

Feel free to open an [issue](https://github.com/leonard112/OctaneScript/issues) if you find any bugs or if you have any feature suggestions.

* __[Source Code](https://github.com/leonard112/OctaneScript)__

* __[Binaries](https://sourceforge.net/projects/octanescript/files/alpha/linux/amd64/dev)__
  
## Linux Installation (amd64 only)

### Debian
> _This package can be installed on any [Debian based Linux distriubtion](https://www.debian.org/derivatives/) including but not limited to __Ubuntu__ and __Kali Linux__._
* Download [Debian package](https://sourceforge.net/projects/octanescript/files/alpha/linux/amd64/dev/debian/) from SourceForge.
```console
$ wget https://pilotfiber.dl.sourceforge.net/project/octanescript/alpha/linux/amd64/dev/debian/octanescript-<version>.deb
```
* Install package.
```console
$ sudo dpkg -i octanescript-<version>.deb
```
* Smoke test.
```console
$ os --version
```
### Tar
_These binaries should work for most Linux distributions._
* Download [tar file](https://sourceforge.net/projects/octanescript/files/alpha/linux/amd64/dev/tar/) from sourceforge.net.
```console
$ wget https://pilotfiber.dl.sourceforge.net/project/octanescript/alpha/linux/amd64/dev/tar/octanescript-<version>.tgz
```
* Create a dedicated folder for the binaries to live.
```console
$ sudo mkdir /opt/octanescript
```
* Extract the contents ot the tar file to the folder where you want the binaries to live.
```console
$ sudo tar -xzvf <file name> --directory /opt/octanescript/
```
* Append the following line to `.bashrc`.
```shell
PATH=/opt/octanescript:$PATH
```
* Smoke test.
```console
$ os --version
```

> _Before Installing Octane on __Windows__, ensure that you have __Python__ installed and __Pip__ package manager installed before you begin. Also ensure that you are running cmd or Powershell as __Administrator__._

> _Note that currently, Octane has to be built on Windows from __source__._

## Windows Installation
* Clone this repository.
```powershell
> git clone https://github.com/leonard112/OctaneScript.git
```
* Navigate to the source code.
```powershell
> cd OctaneScript/src
```
* Install dependencies.
```powershell
> pip install -r requirements.txt
```
* Build os.exe
```powershell
> pyinstaller --onefile  --name os  main.py
```
* Copy everything in the `octane.exe` to your `Program Files (x86)` folder.
```powershell
> mkdir "C:\Program Files (x86)\OctaneScript"`
> cp -r dist/os.exe "C:\Program Files (x86)\OctaneScript\"
```
* Append OctaneScript to `PATH`.
  * https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
* Smoke test.
```powershell
> os --version
```
