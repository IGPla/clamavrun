# ClamAVRun
This script will help you run and automate ClamAV use cases. 

Let's get started:
## Install
 - git clone https://github.com/IGPla/clamavrun.git
 
## Usage
```sh
usage: clamavrun.py [-h] [-i] [-u] [-s] [--scanpath SCANPATH]
                    [--scanoutputfile SCANOUTPUTFILE]

ClamAV antivirus control script

optional arguments:
  -h, --help            show this help message and exit
  -i, --install         Install clamav. Privileged command
  -u, --update          Update ClamAV database
  -s, --scan            Perform scan on the given path
  --scanpath SCANPATH   Path where scan will be performed
  --scanoutputfile SCANOUTPUTFILE
                        Scan output filepath
```
