{
  description = "ytpy";

  inputs = {
      nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
      flake-utils.url = "github:numtide/flake-utils";
   };

  outputs = { self, nixpkgs, flake-utils }:
  flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
         devShells.default = with pkgs; mkShell {
            buildInputs = [
               (python3.withPackages(ps: with ps; [ ffmpeg-python ]))
            ];
         };
      }
   );
}
