
from lulutils import load_jsonl, normalize_text, check_consecutive_words
from collections import defaultdict
from pathlib import Path
import json
import argparse

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", "-i", type=str, required=True)
    parser.add_argument("--output_dir", "-o", type=str)

    parser.add_argument("--response_key", default="prediction", type=str)
    parser.add_argument("--label_key", default="label", type=str)
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
            response = normalize_text(response)
            label = normalize_text(label)
                                   
            correct = check_consecutive_words(long_string=response, short_string=label)
            data["correct"] = correct


    assert datas[0].get(args.group_by_key), f"group_by_key {args.group_by_key} is required"

    group_results = defaultdict(list)
    for data in datas:
        group_results[data[args.group_by_key]].append(data)

    # Print report
    if args.report_mode == "ds":
        group_acc = {}
        task_list = (Path(__file__).resolve().parent / "assets" / "ds.txt")
        for task in task_list.open().readlines():
            task = task.strip()
            if task:
                if group_results.get(f"DS@{task}") is not None:
                    group_acc[f"DS@{task}"] = sum([d["correct"] for d in group_results[f"DS@{task}"]]) / len(group_results[f"DS@{task}"])
                    print(group_acc[f"DS@{task}"])
                else:
                    print("N/A")
            else:
                print()
    else:
        group_acc = {}
        for key, group in group_results.items():
            group_acc[key] = sum([d["correct"] for d in group]) / len(group)
            print(group_acc[key])
        

    report = {
        "input_file": str(args.input_file),
        "output_dir": str(args.output_dir),
        "response_key": args.response_key,
        "label_key": args.label_key,
        "metric": args.metric,
        "report_mode": args.report_mode,
        "results": group_acc,
        "predictions": datas,
    }

    json.dump(report, open(Path(args.output_dir) / f"R@{input_filepath.stem}.json", "w"), ensure_ascii=False, indent=2)

    
        
if __name__ == "__main__":
    args = args_parser()
    main(args)