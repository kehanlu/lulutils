#!/bin/bash
dataset_name=GLOBE_V2_train
input_manifest=/mnt/disk2/hf_share/raw_dataset_manifest/ntu34/GLOBE_V2_train.jsonl
data_root=/mnt/disk2/Datasets/GLOBE_V2/ 
output_dir=/mnt/disk2/hf_share/v3 

python scripts/webdataset/create_shards_from_manifest.py \
    -n $dataset_name \
    -i $input_manifest \
    -o $output_dir \
    --data_root $data_root \
    --require_keys audio_filepath duration


python scripts/huggingface/upload_folder.py \
  --folder ${output_dir}/${dataset_name} \
  --path_in_repo ${dataset_name} \
  --repo_id Morioh/livingroom \
  --revision desta
