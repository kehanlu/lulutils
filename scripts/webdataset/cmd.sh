
PYTHONPATH=/home/hank/research/lulutils
shift=$1
# python examples/webdataset/create_tar_from_manifest.py -n accentDB -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/accentDB.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/Accentdb/accentdb_extended/ --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -n voxceleb1 -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/voxceleb1.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /livingrooms/public/superb/VoxCeleb1 --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/Dailytalk.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/dailytalk -n Dailytalk --shift $shift 

# python examples/webdataset/create_tar_from_manifest.py -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/VCTK.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /groups/public/VCTK-Corpus/ -n VCTK --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/IEMOCAP.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/DeSTA/IEMOCAP/ -n IEMOCAP --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/PromptTTS.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/DeSTA/PromptTTS -n PromptTTS --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/MELD.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/Emobox/MELD.Raw/ -n MELD --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -n MUSAN -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/MUSAN.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/MUSAN_split/ /groups/public/musan/  --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -n Fisher -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/Fisher.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/Fisher/ --shift $shift

# python examples/webdataset/create_tar_from_manifest.py -n Spokenwoz -i /home/khlu/lab/DeSTA3-dev/workspace/250115/manifest/Spokenwoz.jsonl -o /home/khlu/lab/lulutils/workspace --data_root /home/khlu/nas/Datasets/Spokenwoz/ --shift $shift

# python scripts/webdataset/create_tar_from_manifest.py -n GLOBE_V2 -i /mnt/disk2/hf_share/raw_dataset_manifest/ntu34/GLOBE_V2_train.jsonl -o /mnt/disk2/hf_share/v3 --data_root /mnt/disk2/Datasets/GLOBE_V2/ --shift $shift

python scripts/webdataset/create_shards_from_manifest.py -n expresso -i /mnt/disk2/hf_share/raw_dataset_manifest/ntu34/expresso.jsonl -o /mnt/disk2/hf_share/v3 --data_root /mnt/disk2/Datasets/expresso/splits/ --shift $shift