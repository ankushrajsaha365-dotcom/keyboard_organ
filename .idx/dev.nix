# To learn more about how to use Nix to configure your environment
# see: https://firebase.google.com/docs/studio/customize-workspace
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.numpy
    pkgs.python3Packages.sounddevice
    pkgs.python3Packages.pynput
    pkgs.portaudio
    pkgs.xorg.libX11
    pkgs.xorg.libXtst
    pkgs.xorg.libXi
  ];

  # Sets environment variables in the workspace
  env = {};
}