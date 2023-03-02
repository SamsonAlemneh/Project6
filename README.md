# Text Extraction Implementation (Unofficial - Still in Development)

This branch is testing the text extraction and will be kept up-to-date with the add_flask_server_stable_tested branch.

Do not push to this branch; push to add_flask_server_stable_tested branch for updates (this branch is just for testing the text extraction along side the most up-to-date branch without interfering with other people's work - due to specific setup).

## Text Extraction Technology

The text extraction library used is Easyocr: https://github.com/JaidedAI/EasyOCR

## Specific Python Version Needed to Make This Branch Work

One of the prerequisites libaries needed to have Easyocr working (for Windows specifically) is PyTorch: https://pytorch.org/. For non-windows, it seems PyTorch may not be needed (not tested thoroughly, however).

For Windows users that run on Python version 3.11.2 (the latest as of 3/1/2023) and try to download PyTorch by running the following command in the terminal (_note: this command came auto-generated from selected custom options at https://pytorch.org/_):

```
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```

... they come across the following error:

```
ERROR: Could not find a version that satisfies the requirement torch (from versions: none)
ERROR: No matching distribution found for torch
```

Supposedly, the Pytorch library is not supported on higher Python versions, including the latest. See this Stackoverflow post for similar discussion: https://stackoverflow.com/questions/56239310/could-not-find-a-version-that-satisfies-the-requirement-torch-1-0-0.

To combat this, downgrading the Python version is necessary. The following platforms and Python versions were tested and succeeded to have Easyocr (the text extraction library) working as intended:

Windows:

- Python versions: 3.8, 3.9.13

Linux:

- Python versions: 3.9.13

**Note**: Any versions not listed above have not been tested (except the latest 3.11.2; this Python version does not work on Windows; cannot say for non-Windows with 3.11.2).

## To Direct Text Extraction Implementation

- image_extract_text.py: https://github.com/umgc/spring2023/blob/add_flask_server_stable_tested_text_extraction/virotour/flask/app/api/compute/image_extract_text.py
- test_image_extract_text.py: https://github.com/umgc/spring2023/blob/add_flask_server_stable_tested_text_extraction/virotour/flask/app/tests/compute/test_image_extract_text.py
