# HN Part-Time Jobs Parser

A Python script to parse Hacker News "Who is Hiring?" threads and filter for part-time, contract, and freelance opportunities.

## Overview

This tool automatically searches the latest (or a specific) HN "Ask HN: Who is hiring?" thread, downloads all job postings, and filters them for part-time, contract, freelance, and other flexible work arrangements. Results can be displayed in a formatted text view or exported as JSON.

## Features

- 🔍 **Automatic Thread Detection**: Finds the latest "Who is hiring?" thread via Algolia Search API
- ⚡ **Parallel Fetching**: Multi-threaded comment downloading for fast results
- 🎯 **Smart Filtering**: Detects multiple part-time/flexible work keywords
- 📊 **Multiple Output Formats**: Human-readable text or machine-parseable JSON
- 🔧 **Customizable**: Add your own keywords to narrow down results
- 🌳 **Reply Support**: Optionally include nested replies under job postings
- 🛡️ **Robust**: Built-in retry logic and error handling for API calls
- 📝 **Clean Output**: HTML stripping with proper text formatting

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository:

   ```bash
   git clone <repository-url>
   cd parser_agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Find part-time jobs in the latest "Who is hiring?" thread:

```bash
python hn_part_time_jobs.py
```

### Specify a Month

Search a specific month's thread:

```bash
python hn_part_time_jobs.py --month "February 2026"
```

### Additional Keywords

Filter for specific technologies or requirements:

```bash
python hn_part_time_jobs.py --keywords python remote
```

### JSON Output

Export results as JSON for further processing:

```bash
python hn_part_time_jobs.py --json > part_time_jobs.json
```

or

```bash
python hn_part_time_jobs.py --format json --output results.json
```

### Include Nested Replies

Fetch nested comments under each job posting:

```bash
python hn_part_time_jobs.py --include-replies
```

### Verbose Mode

Enable detailed logging for debugging:

```bash
python hn_part_time_jobs.py --verbose
```

## Command-Line Options

| Option              | Description                             | Default       |
| ------------------- | --------------------------------------- | ------------- |
| `--month`           | Target month (e.g., "February 2026")    | Latest thread |
| `--keywords`        | Additional keywords to filter by        | None          |
| `--json`            | Output results as JSON                  | Text format   |
| `--format`          | Output format: `text` or `json`         | `text`        |
| `--workers`         | Number of parallel HTTP workers         | 10            |
| `--include-replies` | Fetch nested replies under postings     | Disabled      |
| `--output`          | Write results to file instead of stdout | stdout        |
| `--verbose`         | Enable verbose logging                  | Disabled      |
| `--version`         | Show version information                | -             |

## Keywords Detected

The script automatically searches for the following keywords:

- **Part-time**: `part time`, `part-time`
- **Contract**: `contract`
- **Freelance**: `freelance`
- **Consulting**: `consulting`
- **Fractional**: `fractional`
- **Flexible**: `flexible hours`, `flexible schedule`
- **Hour-based**: `20 hours/week`, `10-20 hours / week`, etc.
- **Project-based**: `project based`, `project-based`
- **Hourly**: `hourly`

## Output Format

### Text Format (Default)

```
════════════════════════════════════════════════════════════════════════════════
  HN 'Who is Hiring?' — Part-Time Opportunities
  Thread: Ask HN: Who is hiring? (February 2026)
  Results: 42 matches
  Generated: 2026-02-20 14:30
════════════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────────────
🏢 Company X | Senior Developer (Part-Time/Contract)
   👤 username | 📅 2026-02-01 09:15
   🔗 https://news.ycombinator.com/item?id=12345678
   🏷️  Matched: part-time, contract

[Full job posting text...]
```

### JSON Format

```json
[
  {
    "id": 12345678,
    "by": "username",
    "time": 1738403700,
    "url": "https://news.ycombinator.com/item?id=12345678",
    "title": "Company X | Senior Developer (Part-Time/Contract)",
    "matched_keywords": ["part-time", "contract"],
    "text": "Full job posting text..."
  }
]
```

## Examples

### Find remote Python part-time jobs

```bash
python hn_part_time_jobs.py --keywords python remote --format json --output python_jobs.json
```

### Search December 2025 thread with verbose output

```bash
python hn_part_time_jobs.py --month "December 2025" --verbose
```

### Fast search with more workers

```bash
python hn_part_time_jobs.py --workers 20
```

## Dependencies

- **requests** (>=2.25.0): HTTP library with retry support
- **beautifulsoup4** (>=4.9.0): HTML parsing and cleaning
- **urllib3** (>=1.26.0): HTTP client utilities
- **pytest** (>=7.0): Testing framework

See [requirements.txt](requirements.txt) for the complete list.

## Testing

Run the test suite:

```bash
pytest tests/
```

Run tests with verbose output:

```bash
pytest -v tests/
```

## How It Works

1. **Thread Discovery**: Uses Algolia Search API to find the target "Who is hiring?" thread
2. **Comment Fetching**: Retrieves all top-level comments via HN Firebase API
3. **Parallel Processing**: Downloads comments concurrently using ThreadPoolExecutor
4. **Filtering**: Applies regex patterns to match part-time/flexible work keywords
5. **Output Generation**: Formats results as readable text or structured JSON

## API Endpoints Used

- **Algolia Search**: `https://hn.algolia.com/api/v1/search_by_date`
- **HN Firebase**: `https://hacker-news.firebaseio.com/v0/item/{id}.json`

Both APIs are public and don't require authentication.

## Limitations

- Only searches top-level comments by default (use `--include-replies` for nested comments)
- Keyword matching is regex-based and may have false positives
- Rate limiting may occur with very high worker counts
- BeautifulSoup is optional but recommended for better HTML cleaning

## Troubleshooting

### "Could not find a 'Who is hiring?' thread"

Try specifying the month explicitly:

```bash
python hn_part_time_jobs.py --month "January 2026"
```

### Slow performance

Increase the number of workers:

```bash
python hn_part_time_jobs.py --workers 20
```

### Network errors

The script includes automatic retry logic. If issues persist, try running with `--verbose` to see detailed error logs.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Add more keywords
- Improve documentation
- Submit pull requests

## Author

Created for parsing Hacker News job threads efficiently.

---

**Note**: This tool uses public HN APIs and respects rate limits. Please use responsibly.
