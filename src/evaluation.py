import json
from src.pipeline import Pipeline

def evaluate_predictions(truth_links: list[dict], pred_links: list[dict]) -> dict:

    truth_map = {}
    for x in truth_links:
        paragraph_id = x["id"]
        targets = x.get("targetIds", [])
        truth_map[paragraph_id] = set(targets)

    pred_map = {}
    for x in pred_links:
        paragraph_id = x["id"]
        targets = x.get("targetIds", [])
        pred_map[paragraph_id] = set(targets)

    true_positive = 0 
    false_positive = 0
    false_negative = 0
    exact_match = 0

    for paragraph_id in truth_map:
        truth = truth_map[paragraph_id]
        prediction = pred_map.get(paragraph_id, set())

        # correct matches
        true_positive += len(truth & prediction)

        # predicted but not in truth
        false_positive += len(prediction & truth) 

        # missing predictions
        false_negative += len(truth - prediction)

        # exact match
        if truth == prediction:
            exact_match += 1

    total = len(truth_map)

    # metrics
    if true_positive + false_positive == 0:
        precision = 0.0
    else:
        precision = true_positive / (true_positive + false_positive)

    if true_positive + false_negative == 0:
        recall = 0.0
    else:
        recall = true_positive / (true_positive + false_negative)

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    if total == 0:
        exact_match_rate = 0.0
    else:
        exact_match_rate = exact_match / total

    return {
        "total_paragraphs": total,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "exact_match": exact_match,
        "exact_match_rate": exact_match_rate,
    }

def read_data(path:str) -> dict:
    with open(path, mode="r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    input_path = "data/evaluation_data.json"

    data = read_data(input_path)
    pipeline = Pipeline()
    predictions = pipeline.predict(data)

    metrics = evaluate_predictions(
        data.get("paragraphLinks", []),
        predictions.get("paragraphLinks", []),
    )

    print(json.dumps(metrics, indent=2))


    

