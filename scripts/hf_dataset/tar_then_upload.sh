dataset_name=Audiocaps2
input_manifest=/mnt/disk2/hf_share/raw_dataset_manifest/ntu34/Audiocaps2_train.jsonl
output_dir=/mnt/disk2/output_tar # 產生 webdataset 的資料夾, 選一個空間夠的地方
data_root="/mnt/disk2/audiocaps_raw_audio/"  # Dataset 的根目錄，可以有多個


# 準備 webdataset
python scripts/hf_dataset/create_shards_from_manifest.py \
    -n $dataset_name \
    -i $input_manifest \
    -o $output_dir \
    --data_root $data_root \
    --require_keys audio_filepath seed_transcript transcription

# 推到 huggingface
python scripts/hf_dataset/upload_folder.py \
  --folder ${output_dir}/${dataset_name} \
  --path_in_repo ${dataset_name} \
  --repo_id Morioh/livingroom \
  --revision desta