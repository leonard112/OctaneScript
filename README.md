# OctaneScript [![Build Status](https://travis-ci.com/leonard112/OctaneScript.svg?branch=main)](https://travis-ci.com/leonard112/OctaneScript) [![Download OctaneScript](https://img.shields.io/sourceforge/dt/octanescript.svg)](https://sourceforge.net/projects/octanescript/files/alpha/linux/amd64/dev/)

  <img src="https://github.com/leonard112/octane/blob/main/images/octanescript-logo.png" alt="OctaneScript Logo" width=25%></img>

OctaneScript is a scripting language built from Python. OctaneScript is currenly in it's early alpha stages.

:warning: Note that this language is not being developed for any customer or particular use. This lanauge is being developed for fun. Feel free to use this software for whatever you wish, but ensure that you review this software's [license](https://github.com/leonard112/OctaneScript/blob/main/LICENSE) _(MIT)_ if you consider using this software for anything more than exploration and learning. 

Feel free to open an [issue](https://github.com/leonard112/OctaneScript/issues) if you find any bugs or if you have any feature suggestions.

* __[Source Code](https://github.com/leonard112/OctaneScript)__

* __[Release Binaries](https://github.com/leonard112/OctaneScript/releases)__

* __[Development Binaries](https://sourceforge.net/projects/octanescript/files/)__
  
## Linux Installation (amd64 only)

### Debian
> _This package can be installed on any [Debian based Linux distriubtion](https://www.debian.org/derivatives/) including but not limited to __Ubuntu__ and __Kali Linux__._
* Download [Debian package](https://github.com/leonard112/OctaneScript/releases) from the __OctaneScript GitHub Release__ page.
```console
$ wget <OctaneScript Debian dowload URL>
```
* Install package.
```console
$ sudo dpkg -i octanescript-linux-amd64-<version>.deb
```
* Smoke test.
```console
$ os --version
```
### Tar
> _These binaries should work for most Linux distributions._
* Download [tar file](https://github.com/leonard112/OctaneScript/releases) from the __OctaneScript GitHub Release__ page.
```console
$ wget <OctaneScript Tar dowload URL>
```
* Create a dedicated folder for the binaries to live.
```console
$ sudo mkdir /opt/octanescript
```
* Extract the contents ot the tar file to the folder where you want the binaries to live.
```console
$ sudo tar -xzvf octanescript-linux-amd64-<version>.tgz --directory /opt/octanescript/
```
* Append the following line to `.bashrc` to add `/opt/octanescript` to the `PATH` environment variable.
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

### Installer
> _These binaries should work on any 64 bit Windows machine._
* Download [Windows Installer](https://github.com/leonard112/OctaneScript/releases) from the __OctaneScript GitHub Release__ page and Run it.
* Smoke test.
```powershell
> os --version
```

### Zip
> _These binaries should work on any 64 bit Windows machine._

> :warning: _Ensure that you run __Windows PowerShell__ as __Administrator__._
* Download [zip file](https://github.com/leonard112/OctaneScript/releases) from the __OctaneScript GitHub Release__ page.
```powershell
> curl -O <OctaneScript Zip dowload URL>
```
* Create a dedicated folder for the binaries to live.
```powershell
> mkdir "C:\Program Files\OctaneScript" 
```
* Extract the contents ot the zip file to the folder where you want the binaries to live.
```powershell
> Expand-Archive -Path octanescript-windows-amd64-<version>.zip -DestinationPath "C:\Program Files\OctaneScript"
```
* Add `C:\Program Files\OctaneScript\` to the `PATH` environment variable.
  * https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
* Smoke test.
```powershell
> os --version
```
