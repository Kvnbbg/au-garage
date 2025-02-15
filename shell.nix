{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    (python3.withPackages (ps: with ps; [
      pip
      virtualenv
      setuptools
      wheel
    ]))
  ];

  shellHook = ''
    echo "🐍 Environnement Python Nix activé avec $(python --version)"
  '';
}
