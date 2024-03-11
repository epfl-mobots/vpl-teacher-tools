# vpl-teacher-tools

Basic prototypes of VPL teacher tools to test the server

## Build

- In a terminal, cd to the root directory `vpl-teacher-tools` (where this `README.md` file is located)
  ```
  cd "WhereIsYour-vpl-teacher-tools"
- Install [Closure Compiler](https://github.com/google/closure-compiler/wiki/Binary-Downloads) by copying the closure-compiler-vxxxxxxxx.jar file in the root directory `vpl-teacher-tools`
- If using PyEnv or CPython, according to https://github.com/pyenv/pyenv/issues/443#issuecomment-528277145, force to have framework enabled.
  For example with PyEnv, using python 3.9.7 and dedicated virtual env vpl-tt then:
  ```
  env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install -v 3.9.7
  pyenv virtualenv 3.9.7 vpl-tt
  pyenv local vpl-tt
  ```
- Install the required Python packages. In a terminal,
  ```
  python3 -m pip install -U -r requirements.txt
  ```
- On Mac, also install the Objective-C glue:
  ```
  python3 -m pip install -U pyobjc==9.0.1
  ```
- Make the Teacher Tools.
  ```
  make
  ```
