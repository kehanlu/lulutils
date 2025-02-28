
PYTHONPATH=/home/khlu/lab/lulutils
shift=$1

python examples/webdataset/create_shards_from_manifest.py \
    -n dataset_name \
    -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/manifest.jsonl \
    -o /home/khlu/lab/lulutils/workspace \
    --data_root /home/khlu/nas/Datasets/dataset_name/ \
    --shift $shift