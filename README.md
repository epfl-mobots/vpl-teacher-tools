# vpl-teacher-tools

Basic prototypes of VPL teacher tools to test the server

## Build

- Install [Closure Compiler](https://github.com/google/closure-compiler/wiki/Binary-Downloads).
- Install the required Python packages. In a terminal,
  ```
  python3 -m pip install -U -r requirements.txt
  ```
- On Mac, also install the Objective-C glue:
  ```
  python3 -m pip install -U pyobjc==9.0.1
  ```
- Make the Teacher Tools. In a terminal, cd to the root directory `vpl-teacher-tools` (where this `README.md` file is located), then type
  ```
  make
  ```
