from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Union, Literal, Tuple, Optional

from tqdm import tqdm
from tyro.extras import SubcommandApp

from nersemble_data.constants import SERIALS, ASSETS, AVERAGE_GB_PER_VIDEO
from nersemble_data.env import NERSEMBLE_DATA_URL
from nersemble_data.util.download import download_file
from nersemble_data.util.metadata import NeRSembleMetadata
from nersemble_data.util.security import validate_nersemble_data_url

app = SubcommandApp()

AssetType = Literal["calibration", "color_calibration", "images", "meta_data"]


@app.command
def download(
        nersemble_folder: Path,
        /,
        participant: Union[str] = 'all',
        sequence: Union[str] = 'all',
        camera: Union[str] = 'all',
        assets: Union[Literal['all'], Tuple[AssetType, ...]] = 'all',
        n_workers: int = 1):
    """
    Download parts of the NeRSemble dataset

    Parameters
    ----------
    nersemble_folder:
        Where to store the downloaded NeRSemble data
    participant:
        Select which participant(s) to download. Possible values:
            - all: Download all participants
            - range: E.g., "50-100" will only download participants whose ID fall into the specified range
            - comma-separated IDs: E.g., "33,55,77" will only download those 3 participants
    sequence:
        Select which sequence(s) to download  for the specified participant(s). Possible values:
            - all: Download all sequences
            - comma-separated sequence names: E.g., "EXP-1-head,EMO-1-shout+laugh" will only download those 2 sequences
    camera:
        Select which camera(s) to download for the specified participant(s) and sequence(s). Possible values:
            - all: Download all cameras
            - comma-separated camera serials: E.g., "222200037,222200042" will only download those 2 cameras
    assets:
        Which assets to download
    """

    nersemble_metadata = NeRSembleMetadata()
    sequences_per_participant = nersemble_metadata.list_sequences_for_all_participants()

    # ----------------------------------------------------------
    # Filter participants to download
    # ----------------------------------------------------------
    available_participant_ids = nersemble_metadata.list_participants()
    if participant == 'all':
        selected_participant_ids = available_participant_ids
    elif '-' in participant:
        parts = participant.split('-')
        assert len(parts) == 2, f"Invalid --participant specifier, expected a range such as 50-100 but got {participant}"
        id_from = int(parts[0])
        id_to = int(parts[1])
        selected_participant_ids = [p_id for p_id in available_participant_ids if id_from <= p_id <= id_to]
    else:
        parts = participant.split(',')
        selected_participant_ids = [int(p_id) for p_id in parts]
        unavailable_participant_ids = [p_id for p_id in selected_participant_ids if p_id not in available_participant_ids]
        assert len(unavailable_participant_ids) == 0, f"Specified participant_ids do not exist: {unavailable_participant_ids}"

    # ----------------------------------------------------------
    # Filter sequences to download
    # ----------------------------------------------------------
    available_sequences = nersemble_metadata.list_sequences()
    if sequence == 'all':
        selected_sequences = available_sequences
    else:
        selected_sequences = sequence.split(',')
        unavailable_sequences = [seq_name for seq_name in selected_sequences if seq_name not in available_sequences]
        assert len(unavailable_sequences) == 0, f"Specified sequences do not exist: {unavailable_sequences}"

    # ----------------------------------------------------------
    # Filter cameras to download
    # ----------------------------------------------------------
    available_cameras = SERIALS
    if camera == 'all':
        selected_cameras = available_cameras
    else:
        selected_cameras = camera.split(',')
        unavailable_cameras = [serial for serial in selected_cameras if serial not in available_cameras]
        assert len(unavailable_cameras) == 0, f"Specified cameras do not exist: {unavailable_cameras}"

    print("=== DOWNLOAD OVERVIEW ===")
    print(f"Selected {len(selected_participant_ids)} participants: {selected_participant_ids}")
    print(f"Selected {len(selected_sequences)} sequences:")
    for seq_name in selected_sequences:
        print(f" - {seq_name}")
    print(f"Selected {len(selected_cameras)} cameras: {selected_cameras}")
    print(f"Estimated download size: {len(selected_participant_ids) * len(selected_sequences) * len(selected_cameras) * AVERAGE_GB_PER_VIDEO:.1f} GB")
    print(f"Download folder: {nersemble_folder}")
    print("-------------------------")

    answer = input("Proceed? [y/n]")
    if answer == 'y':
        print('Downloading data...')

        # ----------------------------------------------------------
        # Collect download links
        # ----------------------------------------------------------

        if assets == 'all':
            assets = [asset_name for asset_set in ASSETS.values() for asset_name in asset_set.keys()]

        relative_urls = []
        for p_id in selected_participant_ids:
            single_available_sequences = sequences_per_participant[p_id]
            single_selected_sequences = [seq_name for seq_name in selected_sequences if seq_name in single_available_sequences]

            for asset in assets:
                if asset in ASSETS['per_person']:
                    relative_url = ASSETS['per_person'][asset]
                    relative_url = relative_url.format(p_id=p_id)
                    relative_urls.append(relative_url)

            for seq_name in single_selected_sequences:
                for serial in selected_cameras:
                    for asset in assets:
                        if asset in ASSETS['per_cam']:
                            relative_url = ASSETS['per_cam'][asset]
                            relative_url = relative_url.format(p_id=p_id, seq_name=seq_name, serial=serial)
                            relative_urls.append(relative_url)

        # -------------
        # Download data
        # -------------
        if n_workers == 1:
            print(f"[Warning] Downloading data with a single worker which may be slow. Consider setting --n_workers to a number greater than 1")
            for relative_url in tqdm(relative_urls):
                absolute_url = f"{NERSEMBLE_DATA_URL}/{relative_url}"
                target_path = f"{nersemble_folder}/{relative_url}"
                download_file(absolute_url, target_path)
        else:
            print(f"Downloading data with {n_workers} workers")
            pool = ThreadPool(processes=n_workers)
            futures = []
            for relative_url in relative_urls:
                absolute_url = f"{NERSEMBLE_DATA_URL}/{relative_url}"
                target_path = f"{nersemble_folder}/{relative_url}"
                future = pool.apply_async(download_file, (absolute_url, target_path))
                futures.append(future)

            for future in tqdm(futures):
                future.get()


@app.command
def list(participant: Optional[int] = None, /):
    """
    List available participants, or available sequences per participant.

    Parameters
    ----------
    participant: If specified, list the available sequences for the specified participant
    """

    nersemble_metadata = NeRSembleMetadata()
    if participant is None:
        participant_ids = nersemble_metadata.list_participants()
        print("Available participant_ids:")
        print(participant_ids)
    else:
        available_sequences = nersemble_metadata.list_sequences_for_participant(participant)
        print(f"Available sequences for participant {participant}:")
        print(available_sequences)


def main_cli():
    validate_nersemble_data_url()
    app.cli()


if __name__ == '__main__':
    main_cli()
