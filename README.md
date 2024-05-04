# spaghetti
Generate hilariously nonsensical videos. Comes with a selection of funny videos that will be cut, rearranged, and warped in various ways to create something entirely new. You can also add your own videos to the mix.

## Dependencies
- Nix (takes care of dependencies for you)
- VLC/MPV (for video playback; output might not play correctly in other video players)

## How to Use
1. Install Nix:
- Linux: Check your distro's package manager or follow the instructions [here](https://nixos.org/download.html#nix-install-linux).
- MacOS: Follow the instructions [here](https://nixos.org/download.html#nix-install-macos).
- Windows: First, set up [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) if you haven't already. Then, check your distro's package manager or follow the instructions [here](https://nixos.org/download.html#nix-install-windows) within your WSL environment.

2. Clone this repo:
```shell
git clone https://github.com/r3n3gad3p3arl/spaghetti.git
```
3. Enter the development shell:
```shell
cd spaghetti
nix develop
```
4. Optionally, add some of your own videos to the `sources` directory. You can also edit `config.py` and tweak the settings to your liking.

5. Run `main.py`:
```shell
python main.py  # or python3 main.py
```
6. Wait for your video to finish generating. You will find the finished product in the `output` directory.
