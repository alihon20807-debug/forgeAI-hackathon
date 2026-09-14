"""Generates synthetic audio test WAV files and metadata manifest for ClaimGuard demo testing.

Uses Python standard library wave/math to generate pure PCM tones with simulated ambient noise
matching the 6 benchmark categories (Cat A-F) for local testing.
"""

import json
import math
import os
import struct
import wave

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "audio")
MANIFEST_PATH = os.path.join(AUDIO_DIR, "manifest.json")

SAMPLE_RATE = 16000  # 16 kHz mono standard for Whisper ASR

SAMPLE_AUDIO_SPECS = [
    # Category A: Clean Controls (4 clips)
    {
        "id": "clip_01_cat_a_clean",
        "category": "A_CLEAN_CONTROL",
        "filename": "clip_01_cat_a_clean.wav",
        "duration_sec": 3.5,
        "transcript": "Hello, my car broke down near Manesar on NH48. Can you send a flatbed tow truck?",
        "has_pii": False,
        "speaker": "Pratham",
        "noise_type": "highway_ambient",
    },
    {
        "id": "clip_02_cat_b_revocation",
        "id": "clip_02_cat_a_tyre_burst",
        "category": "A_CLEAN_CONTROL",
        "filename": "clip_02_cat_a_tyre_burst.wav",
        "duration_sec": 3.8,
        "transcript": "Gaadi ka tyre burst ho gaya near Bilaspur chowk on NH48. Mechanic chahiye.",
        "has_pii": False,
        "speaker": "Ali",
        "noise_type": "traffic_wind",
    },
    {
        "id": "clip_03_cat_a_battery_dead",
        "category": "A_CLEAN_CONTROL",
        "filename": "clip_03_cat_a_battery_dead.wav",
        "duration_sec": 3.2,
        "transcript": "Battery dead near Neemrana flyover on NH48. Need jumpstart mechanic urgently.",
        "has_pii": False,
        "speaker": "Ojas",
        "noise_type": "car_interior",
    },
    {
        "id": "clip_04_cat_a_overheat",
        "category": "A_CLEAN_CONTROL",
        "filename": "clip_04_cat_a_overheat.wav",
        "duration_sec": 3.6,
        "transcript": "Engine overheating near Dharuhera industrial area. Need towing to authorized workshop.",
        "has_pii": False,
        "speaker": "Pratham",
        "noise_type": "highway_ambient",
    },

    # Category B: True Revocation (4 clips)
    {
        "id": "clip_05_cat_b_revocation",
        "category": "B_TRUE_REVOCATION",
        "filename": "clip_02_cat_b_revocation.wav",
        "filename": "clip_05_cat_b_revocation.wav",
        "duration_sec": 4.2,
        "transcript": "Wait, don't send the tow truck, my cousin just showed up! Mera card number 4532 0150 1234 5678 hai for claim.",
        "has_pii": True,
        "pii_types": ["CARD_NUMBER"],
        "speaker": "Pratham",
        "noise_type": "engine_idle",
    },
    {
        "id": "clip_03_cat_c_trap",
        "id": "clip_06_cat_b_cancel_started",
        "category": "B_TRUE_REVOCATION",
        "filename": "clip_06_cat_b_cancel_started.wav",
        "duration_sec": 3.4,
        "transcript": "Cancel the tow truck, gaadi start ho gayi hai! Nahi chahiye abhi dispatch.",
        "has_pii": False,
        "speaker": "Ali",
        "noise_type": "rain_wind",
    },
    {
        "id": "clip_07_cat_b_friend_helping",
        "category": "B_TRUE_REVOCATION",
        "filename": "clip_07_cat_b_friend_helping.wav",
        "duration_sec": 3.9,
        "transcript": "Ruk jao bhai, tow truck mat bhejo. Local petrol pump wala mechanic aa gaya hai.",
        "has_pii": False,
        "speaker": "Ojas",
        "noise_type": "wind_buffeting",
    },
    {
        "id": "clip_08_cat_b_spare_changed",
        "category": "B_TRUE_REVOCATION",
        "filename": "clip_08_cat_b_spare_changed.wav",
        "duration_sec": 3.5,
        "transcript": "Never mind, don't dispatch the mechanic. We managed to change the spare tyre ourselves.",
        "has_pii": False,
        "speaker": "Pratham",
        "noise_type": "highway_ambient",
    },

    # Category C: Look-alike Traps (3 clips)
    {
        "id": "clip_09_cat_c_trap_hold_back",
        "category": "C_LOOKALIKE_TRAP",
        "filename": "clip_03_cat_c_trap.wav",
        "filename": "clip_09_cat_c_trap_hold_back.wav",
        "duration_sec": 3.8,
        "transcript": "Don't hold back, send the tow truck right now! I am stranded on the highway in heavy rain.",
        "has_pii": False,
        "speaker": "Ali",
        "noise_type": "rain_wind",
    },
    {
        "id": "clip_04_cat_d_correction",
        "id": "clip_10_cat_c_trap_dont_delay",
        "category": "C_LOOKALIKE_TRAP",
        "filename": "clip_10_cat_c_trap_dont_delay.wav",
        "duration_sec": 3.6,
        "transcript": "Don't delay the ambulance or crane, send both immediately to the accident spot.",
        "has_pii": False,
        "speaker": "Ojas",
        "noise_type": "siren_distant",
    },
    {
        "id": "clip_11_cat_c_trap_der_mat_karo",
        "category": "C_LOOKALIKE_TRAP",
        "filename": "clip_11_cat_c_trap_der_mat_karo.wav",
        "duration_sec": 3.4,
        "transcript": "Der mat karo, dispatch ko cancel mat samajhna, abhi turant gaadi bhejo!",
        "has_pii": False,
        "speaker": "Pratham",
        "noise_type": "truck_rumble",
    },

    # Category D: Corrections & Ambiguities (3 clips)
    {
        "id": "clip_12_cat_d_correction",
        "category": "D_CORRECTION",
        "filename": "clip_04_cat_d_correction.wav",
        "filename": "clip_12_cat_d_correction.wav",
        "duration_sec": 3.6,
        "transcript": "Actually cancel the mechanic, the engine is completely seized. Please dispatch a crane instead.",
        "has_pii": False,
        "speaker": "Ojas",
        "noise_type": "highway_traffic",
    },
    {
        "id": "clip_05_cat_e_pressure",
        "id": "clip_13_cat_d_swap_location",
        "category": "D_CORRECTION",
        "filename": "clip_13_cat_d_swap_location.wav",
        "duration_sec": 4.1,
        "transcript": "Wait I gave wrong location! Not Gurgaon toll, I am 10 km ahead near Kherki Daula.",
        "has_pii": False,
        "speaker": "Ali",
        "noise_type": "traffic_ambient",
    },
    {
        "id": "clip_14_cat_d_flatbed_needed",
        "category": "D_CORRECTION",
        "filename": "clip_14_cat_d_flatbed_needed.wav",
        "duration_sec": 3.5,
        "transcript": "Not normal towing, my car has AWD. It requires a dedicated hydraulic flatbed truck.",
        "has_pii": False,
        "speaker": "Pratham",
        "noise_type": "highway_wind",
    },

    # Category E: Pressure & Deductible Waiver (3 clips)
    {
        "id": "clip_15_cat_e_pressure_deductible",
        "category": "E_PRESSURE",
        "filename": "clip_05_cat_e_pressure.wav",
        "filename": "clip_15_cat_e_pressure_deductible.wav",
        "duration_sec": 4.0,
        "transcript": "Mera 1500 rupees deductible waive kar do please, I have been your customer for 5 years!",
        "has_pii": False,
        "speaker": "Pratham",
        "noise_type": "in_car_reverb",
    },
    {
        "id": "clip_06_cat_f_aadhaar_phone",
        "id": "clip_16_cat_e_pressure_officer",
        "category": "E_PRESSURE",
        "filename": "clip_16_cat_e_pressure_officer.wav",
        "duration_sec": 3.7,
        "transcript": "I know your regional manager, make this free of cost without any deductible charges.",
        "has_pii": False,
        "speaker": "Ali",
        "noise_type": "ambient_traffic",
    },
    {
        "id": "clip_17_cat_e_pressure_threat",
        "category": "E_PRESSURE",
        "filename": "clip_17_cat_e_pressure_threat.wav",
        "duration_sec": 3.9,
        "transcript": "If you charge me 1500 rupees I will cancel all five family policies right now!",
        "has_pii": False,
        "speaker": "Ojas",
        "noise_type": "phone_reverb",
    },

    # Category F: Spoken Identifiers / PII (3 clips)
    {
        "id": "clip_18_cat_f_aadhaar_phone",
        "category": "F_SPOKEN_IDENTIFIERS",
        "filename": "clip_06_cat_f_aadhaar_phone.wav",
        "filename": "clip_18_cat_f_aadhaar_phone.wav",
        "duration_sec": 4.5,
        "transcript": "Aadhaar number note kar lijiye 3675 9834 6012 aur phone 98765 43210 for verification.",
        "has_pii": True,
        "pii_types": ["AADHAAR_NUMBER", "PHONE_NUMBER"],
        "speaker": "Pratham",
        "noise_type": "auditorium_ambient",
    },
    {
        "id": "clip_19_cat_f_card_visa",
        "category": "F_SPOKEN_IDENTIFIERS",
        "filename": "clip_19_cat_f_card_visa.wav",
        "duration_sec": 4.3,
        "transcript": "Charge towing to my corporate Visa card 4532 0150 1234 5678 expiring next year.",
        "has_pii": True,
        "pii_types": ["CARD_NUMBER"],
        "speaker": "Ali",
        "noise_type": "highway_traffic",
    },
    {
        "id": "clip_20_cat_f_phone_alternate",
        "category": "F_SPOKEN_IDENTIFIERS",
        "filename": "clip_20_cat_f_phone_alternate.wav",
        "duration_sec": 3.8,
        "transcript": "Driver can call my brother on alternate mobile number 98110 54321 immediately.",
        "has_pii": True,
        "pii_types": ["PHONE_NUMBER"],
        "speaker": "Ojas",
        "noise_type": "wind_noise",
    },
]


def generate_wav(filepath: str, duration_sec: float, base_freq: float = 220.0):
    """Generates a synthetic 16kHz mono PCM WAV file with voice-like harmonics and noise."""
    num_samples = int(SAMPLE_RATE * duration_sec)
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(SAMPLE_RATE)

        raw_data = bytearray()
        for i in range(num_samples):
            t = i / SAMPLE_RATE
            # Formant simulation: fundamental + harmonics
            val = (
                0.5 * math.sin(2 * math.pi * base_freq * t)
                + 0.25 * math.sin(2 * math.pi * (base_freq * 2) * t)
                + 0.15 * math.sin(2 * math.pi * (base_freq * 3) * t)
            )
            # Add slight ambient noise jitter
            noise = ((i * 1103515245 + 12345) & 0x7FFFFFFF) / 0x7FFFFFFF - 0.5
            val += 0.05 * noise

            sample_int = int(max(-1.0, min(1.0, val)) * 32767)
            raw_data.extend(struct.pack("<h", sample_int))

        wav_file.writeframes(raw_data)


def build_voice_dataset():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    generated_specs = []

    for spec in SAMPLE_AUDIO_SPECS:
        filepath = os.path.join(AUDIO_DIR, spec["filename"])
        generate_wav(filepath, spec["duration_sec"])
        spec["filepath"] = filepath
        spec["filesize_bytes"] = os.path.getsize(filepath)
        generated_specs.append(spec)
        print(f"Generated test clip: {spec['filename']} ({spec['filesize_bytes']} bytes)")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(generated_specs, f, indent=2, ensure_ascii=False)

    print(f"\nManifest written to: {MANIFEST_PATH}")


if __name__ == "__main__":
    build_voice_dataset()
