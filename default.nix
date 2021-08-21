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
  preFixup = ''
    substituteInPlace $out/bin/ssh-mv --replace config.yml ${./config.yml}
  '';
  installPhase = "install -m755 -D $src $out/bin/ssh-mv";
}
