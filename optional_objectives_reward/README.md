# Optional Objectives Rewards Mod (SDK v3)

Automatically rewards **ALL** optional objectives in Borderlands 2 and The Pre-Sequel.

## Features

- ✅ **Automatic Detection**: Finds and rewards every optional objective in the game
- ✅ **Playthrough Scaling**: Different rewards for Normal/TVHM/UVHM
- ✅ **Works for both BL2 and TPS**: Auto-detects which game you're playing
- ✅ **Configurable via Mod Menu**: Easy in-game sliders to adjust rewards

## Installation

1. Make sure you have [PythonSDK](https://bl-sdk.github.io/willow2-mod-db/) installed
2. Copy the `optional_objectives_reward.sdkmod` file to your mods folder
3. Enable the mod in the SDK Mod Manager

## Configuration

Open the mod options in-game to configure:

- **Normal Mode Reward**: Percentage for Normal mode (default: 50%)
- **TVHM Reward**: Percentage for TVHM (default: 100%)
- **UVHM Reward**: Percentage for UVHM (default: 200%)

## How It Works

The mod scans all mission definitions in the game and identifies objectives with the `OptionalObjectiveOptionalInfo` property. These are the optional objectives (marked with a different icon in-game). It then applies your configured rewards automatically based on the current playthrough.

## Compatibility

- **Borderlands 2**: ✅ Fully compatible
- **The Pre-Sequel**: ✅ Fully compatible
- **SDK Version**: Requires PythonSDK v3+
- **Multiplayer**: Host only (host needs the mod enabled)

## Building from Source

If you want to build the .sdkmod file yourself:

1. Clone the repository
2. Run the SDK build tools
3. The .sdkmod file will be generated

## Changelog

### Version 1.0 (Initial Release)
- Automatic detection of all optional objectives
- Playthrough-based scaling (Normal/TVHM/UVHM)
- In-game configuration via sliders
- Support for both BL2 and TPS
