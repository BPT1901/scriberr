# Scriberr - A Document Timestamp Cleaner

A Flask web application that removes timestamps from text documents and formats them for better readability. Perfect for cleaning up meeting transcripts and similar documents from virtual meetings or recordings.

## Features

- Upload documents via drag-and-drop or file browser
- Supports .txt, .docx, .vtt files
- Removes various timestamp formats
- Formats text with proper spacing and line breaks
- Real-time processing progress indicator
- Clean, modern web interface
- Network-accessible for local sharing

## Installation

1. Clone the repository
```bash
git clone https://github.com/BPT1901/scriberr.git
cd scriberr
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server
```bash
flask run --host=0.0.0.0 --port=6161
```

2. Access the application:
   - Local machine: http://127.0.0.1:6161
   - Network: http://your-ip-address:6161

3. Upload a document and wait for processing
4. Processed document will automatically download when complete

## Supported Timestamp Formats

The application removes various timestamp formats including:
- [00:00:00]
- 00:00:00.000 --> 00:00:00.000
- (12:34 PM)
- 2024-01-01 15:30:45
- And more...

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)