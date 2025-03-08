dataset_name=MY_COOL_DATASET
input_manifest=/path/to/your_dataset.jsonl
output_dir=/path/to/output/dir # 產生 webdataset 的資料夾, 選一個空間夠的地方
data_root=/path/to/data_root /my/dataset/root  # Dataset 的根目錄，可以有多個

# 準備 webdataset
python scripts/webdataset/create_shards_from_manifest.py \
    -n $dataset_name \
    -i $input_manifest \
    -o $output_dir \
    --data_root $data_root \
    --require_keys audio_filepath transcription duration
