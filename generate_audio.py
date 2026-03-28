import wave
import struct
import math
import random
import os

os.makedirs('assets', exist_ok=True)

def generate_track(filename, duration, tempo, pattern_func):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        chunk_size = 4410
        for i in range(0, num_samples, chunk_size):
            frames = []
            for j in range(chunk_size):
                idx = i + j
                if idx >= num_samples: break
                t = idx / sample_rate
                val = pattern_func(t, tempo)
                val = max(-1.0, min(1.0, val))
                frames.append(struct.pack('<h', int(val * 32767)))
            w.writeframesraw(b''.join(frames))

def battle_pattern(t, bpm):
    beat = t * bpm / 60.0
    bar = int(beat / 4)
    sixteenth = int(beat * 4) % 16
    
    # Drum: Kick and Snare
    drum = 0
    if sixteenth % 8 == 0: 
        drum += math.exp(- (beat * 4 % 8) * 2) * math.sin(2 * math.pi * 60 * t)
    if sixteenth % 8 == 4: 
        drum += math.exp(- (beat * 4 % 8 - 4) * 5) * random.uniform(-1, 1)
    drum += math.exp(- (beat * 2 % 1) * 10) * random.uniform(-0.2, 0.2)
    
    # Bass: Driving 8ths in A minor
    bass_notes = [55.0, 55.0, 55.0, 55.0, 65.41, 65.41, 73.42, 73.42]
    bass_freq = bass_notes[int(beat * 2) % 8]
    if bar % 4 == 3: bass_freq *= 1.2
    bass = 0.5 * math.copysign(1, math.sin(2 * math.pi * bass_freq * t))
    
    # Melody: Syncopated
    melody_notes = [440.0, 0, 523.25, 0, 659.25, 659.25, 0, 880.0, 880.0, 0, 1046.50, 0, 880.0, 0, 659.25, 523.25]
    if bar % 2 == 1:
        melody_notes = [440.0, 523.25, 587.33, 659.25, 0, 659.25, 783.99, 0, 880.0, 0, 0, 880.0, 1046.50, 880.0, 659.25, 523.25]
    m_freq = melody_notes[sixteenth]
    melody = 0
    if m_freq > 0:
        phase = (t * m_freq) % 1.0
        melody = 0.3 if phase < 0.5 else -0.3
        env = math.exp(- (beat * 4 % 1) * 3)
        melody *= env

    return drum * 0.4 + bass * 0.4 + melody * 0.5

def town_pattern(t, bpm):
    beat = t * bpm / 60.0
    bar = int(beat / 3) 
    eighth = int(beat * 2) % 6
    
    progression = [
        [261.63, 329.63, 392.00], # C
        [196.00, 246.94, 293.66], # G
        [220.00, 261.63, 329.63], # Am
        [174.61, 220.00, 261.63], # F
    ]
    chord = progression[bar % 4]
    
    arp_freq = chord[eighth % 3] * 2
    arp = math.sin(2 * math.pi * arp_freq * t) * math.exp(- (beat * 2 % 1) * 2)
    
    bass_freq = chord[0] / 2
    bass = math.sin(2 * math.pi * bass_freq * t) * 0.5
    
    pad = sum([math.sin(2 * math.pi * f * t) for f in chord]) * 0.1
    
    return arp * 0.35 + bass * 0.35 + pad * 0.3

def boss_pattern(t, bpm):
    beat = t * bpm / 60.0
    bar = int(beat / 4)
    sixteenth = int(beat * 4) % 16
    
    drum = 0
    if sixteenth % 4 == 0 or sixteenth == 6 or sixteenth == 10 or sixteenth == 14: 
        drum += math.exp(- (beat * 4 % 1) * 3) * math.sin(2 * math.pi * 50 * t)
    if sixteenth % 8 == 4: 
        drum += math.exp(- (beat * 4 % 8 - 4) * 5) * random.uniform(-1, 1)
        
    bass_notes = [49.00, 49.00, 51.91, 51.91]
    bass_freq = bass_notes[bar % 4]
    bass = 0.6 * math.copysign(1, math.sin(2 * math.pi * bass_freq * t)) * math.exp(- (beat * 2 % 1) * 3)
    
    arp_notes = [196.00, 233.08, 277.18, 329.63]
    arp_freq = arp_notes[sixteenth % 4] * 2
    if bar % 4 == 3: arp_freq *= 1.2 # Tense rise
    arp = 0.4 * math.sin(2 * math.pi * arp_freq * t) * math.exp(- (beat * 4 % 1) * 4)
    
    return drum * 0.5 + bass * 0.5 + arp * 0.4

def clear_pattern(t, bpm):
    beat = t * bpm / 60.0
    bar = int(beat / 4)
    sixteenth = int(beat * 4) % 16
    
    # Triumphant fanfare in C Major
    notes = [523.25, 659.25, 783.99, 1046.50]
    freq = notes[sixteenth % 4]
    if bar >= 1: freq = notes[-(sixteenth % 4) - 1] 
    
    melody = 0.5 * math.sin(2 * math.pi * freq * t) * math.exp(- (beat * 4 % 1) * 3)
    bass = 0.4 * math.sin(2 * math.pi * 130.81 * t)
    
    return melody + bass

def generate_hit():
    sample_rate = 44100
    duration = 0.4
    num_samples = int(sample_rate * duration)
    with wave.open('assets/hit.wav', 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        for i in range(num_samples):
            decay = math.exp(-i / (sample_rate * 0.05))
            value = int(32767 * decay * random.uniform(-1, 1) * 0.5)
            w.writeframesraw(struct.pack('<h', value))

print("Generating Battle BGM...")
generate_track('assets/bgm_battle.wav', 13.714, 140, battle_pattern)
print("Generating Boss BGM...")
generate_track('assets/bgm_boss.wav', 12.0, 160, boss_pattern)
print("Generating Clear BGM...")
generate_track('assets/bgm_clear.wav', 6.0, 160, clear_pattern)
print("Generating Town BGM...")
generate_track('assets/bgm_town.wav', 19.2, 75, town_pattern)
print("Generating SFX...")
generate_hit()
print("Done.")
