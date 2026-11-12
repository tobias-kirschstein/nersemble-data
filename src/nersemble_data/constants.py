from typing import Literal

SERIALS = ["222200042", "222200044", "222200046", "222200040", "222200036", "222200048", "220700191", "222200041",
           "222200037", "222200038", "222200047", "222200043", "222200049", "222200039", "222200045", "221501007"]

SEQUENCE_NAMES = [
    "BACKGROUND",

    "GLASSES",

    "EXP-1-head",
    "EXP-2-eyes",
    "EXP-3-cheeks+nose",
    "EXP-4-lips",
    "EXP-5-mouth",
    "EXP-6-tongue-1",
    "EXP-7-tongue-2",
    "EXP-8-jaw-1",
    "EXP-9-jaw-2",

    "HAIR",

    "FREE",

    "EMO-1-shout+laugh",
    "EMO-2-surprise+fear",
    "EMO-3-angry+sad",
    "EMO-4-disgust+happy",

    "SEN-01-cramp_small_danger",
    "SEN-02-same_phrase_thirty_times",
    "SEN-03-pluck_bright_rose",
    "SEN-04-two_plus_seven",
    "SEN-05-glow_eyes_sweet_girl",
    "SEN-06-problems_wise_chief",
    "SEN-07-fond_note_friend",
    "SEN-08-clothes_and_lodging",
    "SEN-09-frown_events_bad",
    "SEN-10-port_strong_smokey"
]

ASSETS = {
    "global":
        {
            "metadata_participants": "metadata_participants.csv",
            "metadata_sequences": "metadata_sequences.csv",
        },
    "per_person":
        {
            "calibration": "{p_id:03d}/calibration/camera_params.json",
            "color_calibration": "{p_id:03d}/calibration/color_calibration.json"
        },
    "per_sequence":
        {
            "audio": "{p_id:03d}/sequences/{seq_name:}/images/audio_recording.ogg",
        },
    "per_cam":
        {
            "images": "{p_id:03d}/sequences/{seq_name:}/images/cam_{serial:}.mp4",
        },
    "per_person_cam":
        {
            "backgrounds": "{p_id:03d}/sequences/BACKGROUND/image_{serial:}.jpg",
            "backgrounds_olat": "{p_id:03d}/sequences/BACKGROUND_OLAT/images/image_{serial:}.jpg",
        }
}

# Sequences that only contain static background images instead of videos
BACKGROUND_SEQUENCES = ["BACKGROUND", "BACKGROUND_OLAT"]

# Assets that only exist for participants that have the specified (background) sequence
ASSET_REQUIRED_SEQUENCE = {
    "backgrounds_olat": "BACKGROUND_OLAT",
}

# Only sentence sequences come with an audio recording
AUDIO_SEQUENCE_PREFIX = "SEN-"

# ----------------------------------------------------------
# Subsets
# ----------------------------------------------------------
# The NeRSemble dataset consists of several subsets that share the same folder layout:
#   - main: The original NeRSemble v2 data (participants with expressions, emotions and sentences)
#   - hair: Additional recordings focusing on hair motion (participants 601+)

Subset = Literal["main", "hair"]

SUBSET_URL_SUFFIXES = {
    "main": "",
    "hair": "-hair",
}

SERIALS_PER_SUBSET = {
    "main": SERIALS,
    "hair": [serial for serial in SERIALS if serial != "222200047"],  # Camera 222200047 was not used for the hair subset
}

AVERAGE_GB_PER_VIDEO = {
    "main": 1490 / 170631,
    "hair": 0.039,
}

NERSEMBLE_ACCESS_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScYsXR8NVCi4nvmCbFNL0P9swsGodMnbntUJeFejtuKUMsY7Q/viewform"
