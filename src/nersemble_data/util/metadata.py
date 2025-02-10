from typing import List, Optional, Dict

import pandas as pd

from nersemble_data.env import NERSEMBLE_DATA_URL


class NeRSembleMetadata:

    def __init__(self):
        self._metadata_sequences = pd.read_csv(f"{NERSEMBLE_DATA_URL}/metadata_sequences.csv", )

    def list_participants(self) -> List[int]:
        participant_ids = [p_id for p_id in self._metadata_sequences['ID']]
        return participant_ids

    def list_sequences_for_all_participants(self) -> Dict[int, List[str]]:
        participant_ids = self.list_participants()
        sequences_per_participant = dict()
        for participant_id in participant_ids:
            available_sequences = self.list_sequences_for_participant(participant_id)
            sequences_per_participant[participant_id] = available_sequences

        return sequences_per_participant

    def list_sequences_for_participant(self, participant_id: int) -> List[str]:
        participant_row = self._metadata_sequences[self._metadata_sequences['ID'] == participant_id]
        available_sequences = participant_row.apply(lambda row: row[(row == 'x') | (row == 'm')].index, axis=1).tolist()[0].tolist()
        return available_sequences

    def list_sequences(self) -> List[str]:
        return [seq_name for seq_name in self._metadata_sequences.columns if seq_name not in ['ID', 'wears_glasses']]
