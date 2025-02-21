# BAI Assessment Form Generator

A Streamlit application that generates assessment forms for BAI (Brief Alcohol Intervention) and exports them as PDFs.

## Features

- User-friendly web interface
- Input fields for PTID and date
- 15 assessment questions with multiple choice answers
- PDF export functionality
- Vietnamese language support

## Prerequisites

Make sure you have Python installed on your system. Then install the required packages:

```bash
pip install -r requirements.txt
```
## Setup

1. Clone this repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure you have the DejaVu Sans font installed on your system:

For Ubuntu/Debian:
```bash
sudo apt-get install fonts-dejavu
```

For other systems, download and install DejaVu Sans font manually

## Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

## Using the Application

- Enter the PTID (Patient ID)
- Select the completion date
- Answer all 15 questions by selecting one of four options:
  - Không (No)
  - Một chút (A little)
  - Vừa phải (Moderate)
  - Rất nhiều (Very much)
- Click "Xuất PDF" to generate and download the PDF
- The generated PDF will be named "BangHoiDanhGia.pdf"

## Troubleshooting

If you encounter font-related errors:

- Ensure DejaVu Sans font is installed on your system
- The application will fall back to Helvetica if DejaVu Sans is not available

## License

This project is licensed under the MIT License - see the LICENSE file for details.