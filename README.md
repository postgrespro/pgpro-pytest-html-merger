# pgpro-pytest-html-merger
A professional tool to merge multiple pytest-html reports into a single, consistent HTML report. Developed and maintained by Postgres Professional.

## Key Features
- Smart Merging: Combines test results, logs, and metadata from multiple sources.
- Flexible Input: Supports individual files and entire directories.
- Customizable: Set your own report title and output filename.
- Modern Support: Fully compatible with Python 3.8 through 3.14.

## Installation
You can install the package directly from the repository (until it's published to PyPI):
```bash
pip install pgpro-pytest-html-merger
```

## Usage
After installation, the tool is available via the pgpro-pytest-html-merger command.

### Basic Examples
Merge all reports in a directory:
```bash
pgpro-pytest-html-merger -i ./reports -o summary.html
```

Merge specific files with a custom title:
```bash
pgpro-pytest-html-merger report1.html report2.html -o final.html --title "Nightly Build"
```

Combine directories and individual files:
``` bash
pgpro-pytest-html-merger -i ./unit-tests -i ./e2e-tests extra-report.html -o full-report.html
```

### Command Line Arguments

| Argument | Shorthand | Description | Default |
| :--- | :--- | :--- | :--- |
| `--input-dir` | `-i` | Directory containing HTML reports (can be used multiple times) | None |
| `--out` | `-o` | Name of the output HTML report | `merged.html` |
| `--title` | `-t` | Title of the output HTML report | None |
| `--verbose` | `-v` | Level of logging verbosity | 3 |
| `html_files` | | Positional arguments for individual HTML files | None |

## Contributing
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

© 2026 Postgres Professional
