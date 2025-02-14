import os
import pygame
from google.cloud import texttospeech
import time

# Set the environment variable for Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Insert Credentials Path"

def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="de-DE",
        name="de-DE-Neural2-H",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.90  # Set the speaking rate to 75% of the normal speed
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    # Initialize pygame mixer
    pygame.mixer.init()
    # Load and play the audio file
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Stop the mixer and wait a bit to ensure the file is released
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    time.sleep(0.1)  # Add a small delay to ensure the file is released

    # Delete the audio file after playing
    os.remove("output.mp3")
