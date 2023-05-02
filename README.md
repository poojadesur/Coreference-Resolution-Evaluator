# Coreference-Resolution-Evaluator

To Run - 

If input data files contain many documents in a single file,
Run miscell.ipynb to create a new directory for each set of documents - directory names after original file

To run Metrics - 
Run methods.ipynb
If input data contains many documents, and previous step has been followed to create a new directory for each input file, run function get_averaged_scores to get average scores across all these documents.

Parameters for get_averaged_scores - 
gt_dirpath - path to ground truth dir
pred_dirpath - path to pred dir
pred_word_idx - idx in input file where the word exists in the line
pred_annotation_idx - idx in input file where the annotaion exists in the line


