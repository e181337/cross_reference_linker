Cross Reference Linker

This is a small Python prototype for finding internal references in regulatory text and linking them to the correct paragraph IDs.

It tries to:

  detect whether a line is a paragraph, annex, appendix, or figure,

  extract the label at the start of the line,

  find references inside the body text,

  and match those references to real id values in the same document.

It is mainly designed for references like paragraph 2.4, Annex 3, Appendix 2 of Annex 6, and Figure 1.

Project structure

  parser.py: cleans text and splits label/body

  extractor.py: collects references with regex

  indexer.py: builds lookup indexes from document labels

  resolver.py: maps extracted references to target IDs

  pipeline.py: runs the full prediction flow

  evaluation.py: compares predictions with ground truth

The input is a JSON file with text, id, and targetIds fields inside paragraphLinks.
The pipeline returns the same structure, but fills targetIds with predicted links.

This project is intentionally simple: regex-based, easy to read, and built as a lightweight prototype for reference resolution.