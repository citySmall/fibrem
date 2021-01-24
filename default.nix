with (import <nixpkgs> {});
let
  my-python-packages = python-packages: with python-packages; [
    tkinter
    numpy
    natsort
    scikitimage
    matplotlib
    watchdog
    #pywin32
  ];
  python-with-my-packages = python3.withPackages my-python-packages;
in
mkShell {
  buildInputs = [
    python-with-my-packages
  ];
}
