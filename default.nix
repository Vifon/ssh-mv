{ pkgs ? import <nixpkgs> {} }:

with pkgs;
stdenv.mkDerivation rec {
  pname = "ssh-mv";
  version = "1.0.0";
  src = ./ssh_mv.py;

  buildInputs = [
    (python3.withPackages (pyPkgs: with pyPkgs; [
      paramiko
      pyyaml
    ]))
  ];

  dontUnpack = true;
  installPhase = "install -m755 -D $src $out/bin/ssh-mv";
}
