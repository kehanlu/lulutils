
from lulutils import load_jsonl, normalize_text, check_consecutive_words
from collections import defaultdict
from pathlib import Path
import json
import argparse

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str)

    parser.add_argument("--response_key", "prediction", type=str)
    parser.add_argument("--label_key", "label", type=str)
    parser.add_argument("--metric", type=str)

    # report
    parser.add_argument("--report_mode", type=str)
    parser.add_argument("--group_by_key", default="dataset", type=str)
    return parser.parse_args()

def main(args):
    input_filepath = Path(args.input_file)
    if args.output_dir is None:
        args.output_dir = input_filepath.parent

    datas = load_jsonl(args.input_file)
    for data in datas:
        response = data[args.response_key]
        label = data[args.label_key]
        
        if data.get("metric") == "accuracy" or args.metric == "accuracy":
            correct = check_consecutive_words(long_string=response, short_string=label)
            data["correct"] = correct


    assert datas[0].get(args.group_by_key), f"group_by_key {args.group_by_key} is required"

    group_results = defaultdict(list)
    for data in datas:
        group_results[data[args.group_by_key]].append(data)

    # Print report
    if args.report_mode == "ds":
        task_list = (Path(__file__).resolve().parent / "assets" / "ds.txt")
        for task in task_list.open().readlines():
            task = task.strip()
            if task:
                if group_results.get(f"DS@{task}") is not None:
                    print(group_results[f"DS@{task}"])
                else:
                    print("N/A")
            else:
                print()

    report = {
        "input_file": args.input_file,
        "output_dir": args.output_dir,
        "response_key": args.response_key,
        "label_key": args.label_key,
        "metric": args.metric,
        "report_mode": args.report_mode,
        "results": group_results,
        "predictions": datas,
    }

    json.dump(report, open(Path(args.output_dir) / f"R@{input_filepath.stem}.json", "w"), ensure_ascii=False, indent=2)

    
        
if __name__ == "__main__":
    args = args_parser()
    main(args)