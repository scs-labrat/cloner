
# Cloner: Deepfaker Maker

[![GitHub issues](https://img.shields.io/github/issues/yourusername/your-repo.svg)](https://github.com/yourusername/your-repo/issues)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/your-repo.svg)](https://github.com/yourusername/your-repo/stargazers)
[![GitHub license](https://img.shields.io/github/license/yourusername/your-repo.svg)](https://github.com/yourusername/your-repo/blob/master/LICENSE)
[![CLoner](cloner.jpg)]
Cloner is a tool for creating and managing cloned voices using Play.ht's voice cloning API. It allows you to create instant voice clones, generate audio from text, and manage your cloned voices effortlessly.  You need to create an account at play.ht first.

## Features

- Create instant voice clones from audio samples
- Generate audio from text using cloned voices
- List and manage cloned voices
- List and use PlayHT voices

## Installation

### Prerequisites

- Python 3.6+
- Git

### Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/scs-labrat/cloner.git
   cd cloner
   ```

2. **Install the required Python packages**

   ```sh
   pip install -r requirements.txt
   ```

3. **Configure your API credentials**

   Ensure you have your Play.ht `user_id` and `api_key`. You will be prompted to enter these when running the script.

## Usage

1. **Run the script**

   ```sh
   python cloner.py
   ```

2. **Follow the on-screen instructions**

   The script will prompt you to confirm your API credentials and provide options to manage your cloned voices and generate audio.

## Example

Here's an example of how to use Cloner:

1. **List Cloned Voices**

   Select option `1` from the menu to list all your cloned voices.

2. **Create an Instant Clone**

   Select option `3` and provide the path to your audio file and a name for the cloned voice.

3. **Generate Audio with Cloned Voice**

   Select option `4` and follow the prompts to generate audio from text using a cloned voice.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

1. **Fork the repository**
2. **Create a new branch (`git checkout -b feature-branch`)**
3. **Commit your changes (`git commit -am 'Add new feature'`)**
4. **Push to the branch (`git push origin feature-branch`)**
5. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Your Name**
- [GitHub](https://github.com/yourusername)
- [Email](mailto:youremail@example.com)

---

**Disclaimer**: This project is for educational purposes only. Use responsibly.
