{
  description = "nlm-connect development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = [
        pkgs.python311
        pkgs.python311Packages.pip
        pkgs.python311Packages.venvShellHook
      ];
      
      venvDir = "./.venv";
      
      postVenvCreation = ''
        unset SOURCE_DATE_EPOCH
        pip install -r requirements.txt
      '';
      
      postShellHook = ''
        unset SOURCE_DATE_EPOCH
      '';
    };
  };
}
