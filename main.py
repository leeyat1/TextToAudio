from gtts import gTTS
import PyPDF2
import os
from pydub import AudioSegment

# Define the directory containing the PDF files
pdf_directory = '//Users/leeya/Desktop/TextToAudio/PDFs'  # Replace with your PDF files directory
audio_directory = '/Users/leeya/Desktop/TextToAudio/Audios' 

# Function to convert a PDF to text and create an MP3 file
def convert_pdf_to_audio(pdf_filename, output_folder):
    pdf_reader = PyPDF2.PdfReader(open(pdf_filename, 'rb'))

    audio_segments = []

    for page_num in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page_num].extract_text()
        clean_text = text.strip().replace('\n', ' ')

        # Create a gTTS object with the text
        speaker = gTTS(text=clean_text, lang='en')

        # Save the text to an MP3 file
        mp3_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_filename))[0]}_page_{page_num + 1}.mp3")
        speaker.save(mp3_filename)

        # Load the MP3 file as an AudioSegment
        audio_segment = AudioSegment.from_mp3(mp3_filename)
        audio_segments.append(audio_segment)

    return audio_segments

# Process all PDF files in the specified directory
all_audio_segments = []

for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"Processing: {pdf_path}")

        # Convert PDF to audio segments
        pdf_audio_segments = convert_pdf_to_audio(pdf_path, audio_directory)
        all_audio_segments.extend(pdf_audio_segments)

# Concatenate all audio segments into one
final_audio = sum(all_audio_segments)

# Save the final audio to a file
final_audio.export(os.path.join(audio_directory, "final_audio.mp3"), format="mp3")


