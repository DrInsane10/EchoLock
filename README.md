
---

# Echo Lock

Echo Lock is an innovative voice recognition-based security system designed to enhance physical security measures through biometric authentication. Leveraging advanced speech recognition technology, this system provides a secure, keyless entry method by verifying a user's voice against a predefined password. This project utilizes the powerful combination of Python, Vosk for offline voice recognition, and optional integration with Microsoft Cognitive Services for cloud-based enhancements.

## Features

- **Voice Authentication**: Allows users to unlock doors using a voice command, ensuring a hands-free and secure entry.
- **Offline Support**: Utilizes the Vosk API for offline speech recognition, making the system reliable even without internet access.
- **Text-to-Speech Feedback**: Integrates pyttsx3 for providing audible feedback to users during the authentication process.
- **Flexible Integration**: Ready to be integrated with existing security infrastructure or used as a standalone system.
- **Multi-Platform Compatibility**: Designed to run on various hardware setups, ensuring flexibility across different deployment scenarios.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- PyAudio
- Vosk
- pyttsx3
- (Optional) Microsoft Azure subscription for Cognitive Services

### Configuration

- Download and place the Vosk model in the designated directory.
- (Optional) Configure the Microsoft Cognitive Services API by setting the keys in the config file.

### Running the Application

Execute the script from the command line:
```bash
python main.py
```

## Usage

After running the application, speak your predefined password into the microphone. The system will verify your voice and provide audio feedback whether access is granted or denied.


## Contact
[Rishabh Dhiman](rishabhdhiman10@gmail.com)

---
