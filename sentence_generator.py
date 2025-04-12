import pygame
import random
from gtts import gTTS
import os
import tempfile

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sentence Generator')

# Font setup
FONT = pygame.font.SysFont('Arial', 24)
TITLE_FONT = pygame.font.SysFont('Arial', 36)

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

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, surface):
        color = self.color if not self.is_hovered else LIGHT_BLUE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def generate_sentence():
    return random.choice(german_sentences)

def speak_sentence(sentence):
    # Create a temporary file for the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Generate speech using gTTS with German language
        tts = gTTS(text=sentence, lang='de')
        tts.save(temp_filename)
        
        # Play the audio using pygame mixer
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_filename)
        except:
            pass

def main():
    button = Button(
        WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
        WINDOW_HEIGHT // 2 - BUTTON_HEIGHT // 2,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Nächster Satz",
        BLUE
    )
    
    current_sentence = ""
    last_sentence = ""  # Track the last spoken sentence
    running = True
    last_sentence_time = 0
    sentence_delay = 1000  # 1 second delay before speaking
    
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if button.handle_event(event):
                current_sentence = generate_sentence()
                last_sentence_time = current_time
                last_sentence = ""  # Reset last spoken sentence when generating new one
        
        # Draw everything
        screen.fill(WHITE)
        
        # Draw title
        title = TITLE_FONT.render("Deutsche Literatur", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw button
        button.draw(screen)
        
        # Draw current sentence
        if current_sentence:
            # Split long sentences into multiple lines if needed
            words = current_sentence.split()
            lines = []
            current_line = []
            max_width = WINDOW_WIDTH - 100
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                if FONT.size(test_line)[0] > max_width:
                    if len(current_line) > 1:
                        lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw each line
            for i, line in enumerate(lines):
                sentence_surface = FONT.render(line, True, BLACK)
                sentence_rect = sentence_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100 + i * 30))
                screen.blit(sentence_surface, sentence_rect)
            
            # Speak the sentence after the delay, but only if it hasn't been spoken before
            if (current_time - last_sentence_time >= sentence_delay and 
                not pygame.mixer.music.get_busy() and 
                current_sentence != last_sentence):
                speak_sentence(current_sentence)
                last_sentence = current_sentence  # Mark this sentence as spoken
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main() 