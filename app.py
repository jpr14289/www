from flask import Flask, render_template, jsonify, send_file
from gtts import gTTS
import random
import os
import tempfile

app = Flask(__name__)

# Real German sentences from literature
german_sentences = [
    "Der Mensch ist ein Seil, geknüpft zwischen Tier und Übermensch.",  # Nietzsche
    "Es ist ein befremdliches Gefühl, wenn man zum ersten Mal in seinem Leben allein ist.",  # Kafka
    "Die Welt ist voll von Dingen, die darauf warten, entdeckt zu werden.",  # Goethe
    "Das Leben ist zu kurz für lange Gesichter.",  # Schiller
    "Man sieht nur mit dem Herzen gut. Das Wesentliche ist für die Augen unsichtbar.",  # Saint-Exupéry
    "Die Zeit ist ein großer Lehrer, aber leider tötet sie alle ihre Schüler.",  # Berlioz
    "Glück ist das einzige, was sich verdoppelt, wenn man es teilt.",  # Albert Schweitzer
    "Die Sprache ist die Kleidung der Gedanken.",  # Lichtenberg
    "Wer die Musik liebt, kann nie ganz unglücklich werden.",  # Hesse
    "Das Leben ist wie ein Fahrrad. Man muss sich vorwärts bewegen, um das Gleichgewicht nicht zu verlieren.",  # Einstein
    "Die Wahrheit ist wie die Sonne. Man kann sie eine Zeit lang ausschließen, aber nicht auf Dauer.",  # Goethe
    "Ein Buch muss die Axt sein für das gefrorene Meer in uns.",  # Kafka
    "Die Kunst ist eine Vermittlerin des Unaussprechlichen.",  # Goethe
    "Man muss noch Chaos in sich haben, um einen tanzenden Stern gebären zu können.",  # Nietzsche
    "Die beste Zeit, einen Baum zu pflanzen, war vor zwanzig Jahren. Die nächstbeste Zeit ist jetzt.",  # Chinesisches Sprichwort
    "Das Glück ist wie ein Schmetterling. Je mehr du es jagst, desto mehr entwischt es dir.",  # Goethe
    "Die Welt ist ein Buch. Wer nie reist, sieht nur eine Seite davon.",  # Augustinus
    "Die größte Kunst ist, den Augenblick festzuhalten.",  # Goethe
    "Das Leben ist wie ein Theaterstück: Es kommt nicht darauf an, wie lang es ist, sondern wie bunt.",  # Seneca
    "Die Zeit heilt alle Wunden, aber sie ist ein schlechter Kosmetiker.",  # Twain
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    sentence = random.choice(german_sentences)
    return jsonify({'sentence': sentence})

@app.route('/speak/<sentence>')
def speak(sentence):
    # Create a temporary file for the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Generate speech using gTTS with German language
        tts = gTTS(text=sentence, lang='de')
        tts.save(temp_filename)
        
        # Send the file to the client
        return send_file(
            temp_filename,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='sentence.mp3'
        )
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_filename)
        except:
            pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 