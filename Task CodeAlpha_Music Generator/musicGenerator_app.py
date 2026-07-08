# # music_app.py
# import streamlit as st
# import numpy as np
# import random
# from midiutil import MIDIFile
# import base64
# import os
#
# st.set_page_config(page_title="Music Generator", page_icon="🎵")
#
# st.title("🎵 AI Music Generator")
# st.markdown("---")
#
# # Music theory
# notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# scales = {
#     'C Major': [0, 2, 4, 5, 7, 9, 11],
#     'A Minor': [9, 11, 0, 2, 3, 5, 7],
#     'G Major': [7, 9, 11, 0, 2, 4, 5],
# }
#
# # Sidebar controls
# with st.sidebar:
#     st.header("Settings")
#     scale = st.selectbox("Scale", list(scales.keys()))
#     length = st.slider("Melody Length", 4, 32, 8)
#     tempo = st.slider("Tempo (BPM)", 60, 180, 120)
#
#     generate = st.button("Generate Melody", type="primary", use_container_width=True)
#
# # Main area
# col1, col2 = st.columns(2)
#
# if generate:
#     # Generate melody
#     scale_notes = scales[scale]
#     melody = []
#
#     for i in range(length):
#         note_idx = random.choice(scale_notes)
#         octave = 4 if random.random() < 0.8 else 5
#         note = f"{notes[note_idx % 12]}{octave}"
#         melody.append(note)
#
#     # Display in columns
#     with col1:
#         st.subheader("Generated Melody")
#         st.code(" → ".join(melody))
#
#         # Note sequence
#         st.subheader("Note Sequence")
#         for i, note in enumerate(melody):
#             st.text(f"Note {i + 1}: {note}")
#
#     with col2:
#         st.subheader("Visualization")
#
#         # Simple visualization
#         chart_data = []
#         for note in melody:
#             # Convert note to number for visualization
#             note_name = note[:-1]
#             octave = int(note[-1])
#             note_num = notes.index(note_name) + (octave * 12)
#             chart_data.append(note_num)
#
#         st.line_chart(chart_data)
#
#         # Create MIDI
#         midi = MIDIFile(1)
#         track = 0
#         time = 0
#         midi.addTempo(track, time, tempo)
#
#         for i, note_str in enumerate(melody):
#             note_name = note_str[:-1]
#             octave = int(note_str[-1])
#             pitch = 60 + (notes.index(note_name) - 3) + (octave - 4) * 12
#             midi.addNote(track, 0, pitch, time + i, 1, 100)
#
#         # Save and provide download
#         midi_file = "melody.mid"
#         with open(midi_file, "wb") as f:
#             midi.writeFile(f)
#
#         with open(midi_file, "rb") as f:
#             midi_bytes = f.read()
#             b64 = base64.b64encode(midi_bytes).decode()
#             href = f'<a href="data:audio/midi;base64,{b64}" download="melody.mid">⬇️ Download MIDI</a>'
#             st.markdown(href, unsafe_allow_html=True)
#
#         os.remove(midi_file)

# ultra_fast_music_generator.py



import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import time


class UltraFastMusicGenerator:
    def __init__(self):
        # Tiny synthetic dataset
        self.create_toy_dataset()
        self.build_model()

    def create_toy_dataset(self):
        """Create a tiny synthetic dataset"""
        print("Creating toy dataset...")

        # Simple patterns (C major scale patterns)
        self.notes = [
                         'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5',
                         'C4', 'E4', 'G4', 'C5', 'E4', 'G4', 'C4',
                         'G4', 'B4', 'D5', 'G5', 'B4', 'D5', 'G4',
                         'C4', 'F4', 'A4', 'C5', 'F4', 'A4', 'C4',
                     ] * 5  # Repeat to create more data

        # Create mappings
        self.unique_notes = sorted(set(self.notes))
        self.note_to_int = {n: i for i, n in enumerate(self.unique_notes)}
        self.int_to_note = {i: n for i, n in enumerate(self.unique_notes)}
        self.n_vocab = len(self.unique_notes)

        print(f"Dataset: {len(self.notes)} notes, {self.n_vocab} unique")

    def build_model(self):
        """Build tiny LSTM"""
        self.model = Sequential([
            LSTM(32, input_shape=(10, 1)),
            Dense(16, activation='relu'),
            Dense(self.n_vocab, activation='softmax')
        ])
        self.model.compile(loss='sparse_categorical_crossentropy',
                           optimizer='adam', metrics=['accuracy'])

    def prepare_data(self):
        """Prepare sequences"""
        X, y = [], []
        seq_length = 10

        for i in range(len(self.notes) - seq_length):
            X.append([self.note_to_int[n] for n in self.notes[i:i + seq_length]])
            y.append(self.note_to_int[self.notes[i + seq_length]])

        X = np.array(X).reshape(len(X), seq_length, 1)
        y = np.array(y)

        return X, y

    def train(self, epochs=10):
        """Train ultra fast"""
        X, y = self.prepare_data()

        print(f"Training on {len(X)} sequences...")
        start = time.time()

        history = self.model.fit(X, y, epochs=epochs, verbose=1)

        train_time = time.time() - start
        print(f"✅ Trained in {train_time:.2f} seconds!")
        print(f"Final accuracy: {history.history['accuracy'][-1]:.2%}")

        return history

    def generate(self, seed=None, length=20):
        """Generate melody"""
        if seed is None:
            seed = self.notes[:10]

        pattern = [self.note_to_int[n] for n in seed]
        generated = []

        for _ in range(length):
            x = np.array(pattern[-10:]).reshape(1, 10, 1)
            pred = self.model.predict(x, verbose=0)[0]

            # Add some randomness
            if np.random.random() < 0.3:
                idx = np.argmax(pred)
            else:
                idx = np.random.randint(0, self.n_vocab)

            note = self.int_to_note[idx]
            generated.append(note)
            pattern.append(idx)

        return generated


# Run
print("🚀 Ultra-Fast Training (10-15 minutes)")
generator = UltraFastMusicGenerator()
generator.train(epochs=20)
melody = generator.generate()
print("\n🎵 Generated:", " → ".join(melody))
