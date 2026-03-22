# Cross Reference Linker

This repository contains a small rule-based system for detecting internal references in regulatory text and resolving them to paragraph IDs within the same document.

The goal was not to build a heavy NLP pipeline, but to put together a working and readable prototype that can:

- identify structural items such as paragraphs, annexes, appendices, and figures
- extract internal references from paragraph text
- match those references to the correct target IDs in the same JSON document

## Approach

The solution is organized as a simple pipeline:

1. `parser.py`
Parses each paragraph, detects its record type, extracts the label, and separates the body text.

2. `indexer.py`
Builds lookup tables from the parsed document so references can later be resolved to paragraph IDs.

3. `extractor.py`
Uses regex patterns to find references such as:
- `paragraph 2.4`
- `paragraphs 8.24.5.1.5 and 8.24.5.1.8`
- `Annex 3`
- `Appendix 2 of Annex 6`
- `Figure 1`

4. `resolver.py`
Maps extracted references to the matching IDs using the lookup tables.

5. `pipeline.py`
Runs the full end-to-end prediction flow and writes the output JSON.

6. `evaluation.py`
Runs the pipeline on the reference dataset and computes evaluation metrics.

## Repository Structure

- [src/parser.py](/Users/erinckoc/Desktop/Code/cross-reference-linker/src/parser.py)
- [src/indexer.py](/Users/erinckoc/Desktop/Code/cross-reference-linker/src/indexer.py)
- [src/extractor.py](/Users/erinckoc/Desktop/Code/cross-reference-linker/src/extractor.py)
- [src/resolver.py](/Users/erinckoc/Desktop/Code/cross-reference-linker/src/resolver.py)
- [src/pipeline.py](/Users/erinckoc/Desktop/Code/cross-reference-linker/src/pipeline.py)
- [src/evaluation.py](/Users/erinckoc/Desktop/Code/cross-reference-linker/src/evaluation.py)
- [data/evaluation_data.json](/Users/erinckoc/Desktop/Code/cross-reference-linker/data/evaluation_data.json)
- [data/test_data.json](/Users/erinckoc/Desktop/Code/cross-reference-linker/data/test_data.json)

## Input Format

Both datasets follow the same structure:

```json
{
  "documentVersionKey": "...",
  "documentVersionId": "...",
  "rootRegion": "...",
  "region": "...",
  "paragraphLinks": [
    {
      "text": "3.2.1. ... paragraph 2.4. ...",
      "id": "paragraph-id-1",
      "targetIds": []
    }
  ]
}
```

The pipeline returns the same structure, but with predicted values in `targetIds`.

## How To Run

Run evaluation on the reference dataset:

```bash
python3 -m src.evaluation
```

Generate predictions for the test dataset:

```bash
python3 -m src.pipeline
```

This writes the output file to:

- [data/test_predictions.json](/Users/erinckoc/Desktop/Code/cross-reference-linker/data/test_predictions.json)

## Current Result

On the reference dataset, the current implementation produces:

- precision: `0.50`
- recall: `0.476`
- f1: `0.4875`
- exact match rate: `0.9543`

On the test set, the generated prediction file contains 298 paragraphs, with predicted references for 68 of them.
