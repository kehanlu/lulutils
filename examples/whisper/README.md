## Run Whisper ASR

- `--input_filelist`, -i (required): Path to a text file containing absolute filepaths of audio files, one per line.
- `--output_path`, -o (required): Path for the output JSONL file containing ASR results.
- `--whisper_id` (optional): ID of the Whisper model to use. Default: "openai/whisper-large-v3"
- `--batch_size` (optional): Number of audio files to process in each batch. Default: 16

```
python examples/whisper/run_asr.py -i examples/whisper/audio_filelist.txt -o examples/whisper/outputs.jsonl
```