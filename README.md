# Drifter Scanner

An EVE Online companion app that monitors local chat logs to detect drifter wormhole connections and reports them to a [DrifterbearAA](https://github.com/spapin/drifterbearaa) Alliance Auth server.

## How It Works

Drifter Scanner runs as a Windows system tray application. It watches your EVE Online chat log files for player jumps from known drifter wormhole systems, identifies the drifter type based on the system name, and posts the connection data to your configured DrifterbearAA callback URL.

### Supported Drifter Types

Barbican, Conflux, Redoubt, Sentinel, Vidette

## Installation

Download the latest installer from [GitHub Releases](https://github.com/spapin/drifter_scanner/releases) and run it. No additional dependencies are required.

## Configuration

1. Right-click the Drifter Scanner icon in your system tray
2. Select **Set Callback URL** and enter your DrifterbearAA callback URL
3. Configuration is stored at `~/.drifter_scanner/config.json`

## Building from Source

### Prerequisites

- Python 3.12+
- [Inno Setup](https://jrsoftware.org/isinfo.php) (for building the installer)

### Steps

```bash
# Clone the repository
git clone https://github.com/spapin/drifter_scanner.git
cd drifter_scanner

# Install dependencies
pip install -e .
pip install pyinstaller

# Build the executable
pyinstaller drifter-scanner.spec

# Build the installer (requires Inno Setup)
iscc installer.iss
```

The installer will be output to the `Output/` directory.

## Releasing

Pushing a version tag triggers GitHub Actions to build the executable, package the installer, and create a release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The release will include both `DrifterScannerSetup.exe` (installer) and `drifter-scanner-portable.exe`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
