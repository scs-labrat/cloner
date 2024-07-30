import requests
import pyfiglet
from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize colorama
init(autoreset=True)

# Define the client details
user_id = ""
api_key = ""

base_url = "https://api.play.ht/api/v2"

# Headers for requests
headers = {
    "accept": "application/json",
    "Authorization": api_key,
    "X-User-Id": user_id
}

cloned_voices = []
playht_voices = []

def print_banner():
    banner = pyfiglet.figlet_format("Cloner", font="poison")
    tagline = pyfiglet.figlet_format("Deepfaker Maker     --     d8rh8r", font="digital")
    
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.WHITE + tagline + Style.RESET_ALL)

def format_voices(voices):
    table_data = []
    for index, voice in enumerate(voices):
        name = voice.get('name', 'N/A')
        language = voice.get('language', 'N/A')
        gender = voice.get('gender', 'N/A')
        voice_id = voice.get('id', 'N/A')
        table_data.append([index, name, language, gender, voice_id])
    table = tabulate(table_data, headers=["Index", "Name", "Language", "Gender", "ID"], tablefmt="grid")
    print(Fore.GREEN + table)

def list_cloned_voices():
    global cloned_voices
    url = f"{base_url}/cloned-voices"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        cloned_voices = response.json()
        format_voices(cloned_voices)
    else:
        print(Fore.RED + f"Failed to list cloned voices: {response.status_code} {response.text}")

def delete_cloned_voice():
    voice_id = input(Fore.YELLOW + "Please provide the ID of the cloned voice to delete: ")
    if not voice_id:
        print(Fore.RED + "No voice ID provided. Please try again.")
        return
    
    url = f"{base_url}/cloned-voices/{voice_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + "Cloned voice successfully deleted.")
    else:
        print(Fore.RED + f"Failed to delete cloned voice: {response.status_code} {response.text}")

def create_instant_clone():
    sample_file_path = input(Fore.YELLOW + "Please provide the path to the sample file (e.g., 'graig.wav'): ")
    voice_name = input(Fore.YELLOW + "Please provide a name for the new cloned voice: ")

    if not sample_file_path or not voice_name:
        print(Fore.RED + "No file path or voice name provided. Please try again.")
        return

    url = f"{base_url}/cloned-voices/instant"
    try:
        with open(sample_file_path, "rb") as file:
            files = {"sample_file": (sample_file_path, file, "audio/wav")}
            data = {"voice_name": voice_name}
            
            response = requests.post(url, files=files, headers=headers, data=data)
            print(response.text)

    except FileNotFoundError:
        print(Fore.RED + f"File '{sample_file_path}' not found. Please check the file path and try again.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

def list_playht_voices():
    global playht_voices
    url = f"{base_url}/voices"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        playht_voices = response.json()
        format_voices(playht_voices)
    else:
        print(Fore.RED + f"Failed to list PlayHT voices: {response.status_code} {response.text}")

def create_audio_with_cloned_voice():
    if not cloned_voices:
        print(Fore.RED + "No cloned voices available. Please list cloned voices first.")
        return

    text = input(Fore.YELLOW + "Please provide the text to convert to speech: ")
    voice_index = int(input(Fore.YELLOW + "Please provide the index of the cloned voice: "))
    if voice_index < 0 or voice_index >= len(cloned_voices):
        print(Fore.RED + "Invalid voice index. Please try again.")
        return
    voice_id = cloned_voices[voice_index]['id']

    quality = input(Fore.YELLOW + "Please provide the quality (e.g., draft, low, medium, high, premium) [default: medium]: ") or "medium"
    output_format = input(Fore.YELLOW + "Please provide the output format (e.g., mp3, wav, ogg, flac, mulaw) [default: mp3]: ") or "mp3"
    speed = float(input(Fore.YELLOW + "Please provide the speed (0.1 to 5) [default: 1]: ") or "1")
    sample_rate = int(input(Fore.YELLOW + "Please provide the sample rate (8000 to 48000) [default: 24000]: ") or "24000")
    seed = input(Fore.YELLOW + "Please provide the seed (>=0) [default: null]: ")
    temperature = float(input(Fore.YELLOW + "Please provide the temperature (0 to 2) [default: 1]: ") or "1")
    voice_engine = input(Fore.YELLOW + "Please provide the voice engine (PlayHT1.0 or PlayHT2.0) [default: PlayHT2.0]: ") or "PlayHT2.0"
    emotion = input(Fore.YELLOW + "Please provide the emotion (optional, e.g., female_happy, male_sad): ") or None
    voice_guidance = input(Fore.YELLOW + "Please provide the voice guidance (1 to 6) [optional]: ")
    style_guidance = input(Fore.YELLOW + "Please provide the style guidance (1 to 30) [optional]: ")

    # Validate and process optional parameters
    if not seed:
        seed = None
    if not voice_guidance:
        voice_guidance = None
    if not style_guidance:
        style_guidance = None

    allowed_emotions = [
        "female_happy", "female_sad", "female_angry", "female_fearful", "female_disgust", "female_surprised",
        "male_happy", "male_sad", "male_angry", "male_fearful", "male_disgust", "male_surprised", None
    ]

    if emotion not in allowed_emotions:
        print(Fore.RED + f"Invalid emotion. Allowed values are: {', '.join(allowed_emotions)}.")
        return

    url = f"{base_url}/tts"
    data = {
        "text": text,
        "voice": voice_id,
        "quality": quality,
        "output_format": output_format,
        "speed": speed,
        "sample_rate": sample_rate,
        "seed": seed,
        "temperature": temperature,
        "voice_engine": voice_engine,
        "emotion": emotion,
        "voice_guidance": voice_guidance,
        "style_guidance": style_guidance
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(Fore.GREEN + "TTS job successfully created.")
        print(response.json())
    else:
        print(Fore.RED + f"Failed to create TTS job: {response.status_code} {response.text}")

def create_audio_with_playht_voice():
    if not playht_voices:
        print(Fore.RED + "No PlayHT voices available. Please list PlayHT voices first.")
        return

    text = input(Fore.YELLOW + "Please provide the text to convert to speech: ")
    voice_index = int(input(Fore.YELLOW + "Please provide the index of the PlayHT voice: "))
    if voice_index < 0 or voice_index >= len(playht_voices):
        print(Fore.RED + "Invalid voice index. Please try again.")
        return
    voice_id = playht_voices[voice_index]['id']

    quality = input(Fore.YELLOW + "Please provide the quality (e.g., draft, low, medium, high, premium) [default: medium]: ") or "medium"
    output_format = input(Fore.YELLOW + "Please provide the output format (e.g., mp3, wav, ogg, flac, mulaw) [default: mp3]: ") or "mp3"
    speed = float(input(Fore.YELLOW + "Please provide the speed (0.1 to 5) [default: 1]: ") or "1")
    sample_rate = int(input(Fore.YELLOW + "Please provide the sample rate (8000 to 48000) [default: 24000]: ") or "24000")
    seed = input(Fore.YELLOW + "Please provide the seed (>=0) [default: null]: ")
    temperature = float(input(Fore.YELLOW + "Please provide the temperature (0 to 2) [default: 1]: ") or "1")

    # Validate and process optional parameters
    if not seed:
        seed = None

    url = f"{base_url}/tts"
    data = {
        "text": text,
        "voice": voice_id,
        "quality": quality,
        "output_format": output_format,
        "speed": speed,
        "sample_rate": sample_rate,
        "seed": seed,
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(Fore.GREEN + "TTS job successfully created.")
        print(response.json())
    else:
        print(Fore.RED + f"Failed to create TTS job: {response.status_code} {response.text}")

def confirm_credentials():
    global user_id, api_key, headers
    print(Fore.CYAN + "Current credentials:")
    print(Fore.CYAN + f"User ID: {user_id}")
    print(Fore.CYAN + f"API Key: {api_key}")
    confirm = input(Fore.YELLOW + "Do you want to use these credentials? (yes/no): ").strip().lower()
    if confirm != 'yes':
        user_id = input(Fore.YELLOW + "Please enter your User ID: ").strip()
        api_key = input(Fore.YELLOW + "Please enter your API Key: ").strip()
        headers = {
            "accept": "application/json",
            "Authorization": api_key,
            "X-User-Id": user_id
        }

def main():
    confirm_credentials()
    print_banner()
    while True:
        print(Fore.CYAN + "\nMenu:" + Style.RESET_ALL)
        print(Fore.CYAN + "1. List Cloned Voices" + Style.RESET_ALL)
        print(Fore.CYAN + "2. Delete Cloned Voice" + Style.RESET_ALL)
        print(Fore.CYAN + "3. Create Instant Clone" + Style.RESET_ALL)
        print(Fore.CYAN + "4. Create Audio with Cloned Voice" + Style.RESET_ALL)
        print(Fore.CYAN + "5. List PlayHT Voices" + Style.RESET_ALL)
        print(Fore.CYAN + "6. Create Audio with PlayHT Voice" + Style.RESET_ALL)
        print(Fore.CYAN + "7. Exit" + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "Please choose an option: " + Style.RESET_ALL)

        if choice == "1":
            list_cloned_voices()
        elif choice == "2":
            delete_cloned_voice()
        elif choice == "3":
            create_instant_clone()
        elif choice == "4":
            create_audio_with_cloned_voice()
        elif choice == "5":
            list_playht_voices()
        elif choice == "6":
            create_audio_with_playht_voice()
        elif choice == "7":
            print(Fore.GREEN + "Exiting..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
