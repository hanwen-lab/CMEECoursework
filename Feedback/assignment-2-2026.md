# Assignment 2 formative feedback

This feedback is organised by the relevant computing bootcamp criteria. Use it to decide what is already working, what you need to investigate, and what to revise before the cumulative submission.

The full criteria are in the [Computing Bootcamp assessment rubric](https://github.com/MulQuaBio/MQB/blob/main/content/rubrics/Computing_Bootcamp_Rubric.md).

## 1. Repository organisation and workflow discipline

- Your root README, `.gitignore`, cleaning script, test script and supplied data files are in the expected locations. The supplied CSV and metadata are unchanged, giving you a reproducible starting point.

## 2. Code completeness and functional correctness

- The cleaning workflow executed successfully. Separately, output checks found that all three output tables satisfied the requirements on both test runs. The outputs are correct for the checked input; now make sure you can explain how your functions produce them.
- Run the separate tests and cleaning script again after any edits, checking all three generated tables.

## 3. Code quality and style

- Your `main()` function gives the program a clear overall structure by connecting loading, processing, summarising and writing. Keep these stages distinct as you revise; use descriptive names and add short comments where the reason for a validation check or data-cleaning step is not obvious.

## 4. Documentation

- Your root README is in place. Make it useful to someone opening the repository for the first time: explain what the cleaner does, how to run the script and tests from the repository root, and which three files it creates. Test the instructions in a newly cloned copy of your repository (a separate folder created with `git clone`): enter that folder and run each README command exactly as written. If something fails, correct the command or add the missing step.

## 5. Version-control practice

- Since the previous formative feedback was added, the saved history contains 1 non-merge commit. Assignment 2 appears in one recent commit, `Complete Silwood tree survey cleaning`. This records a finished snapshot, but not the stages used to reach it.
- For the final revisions, avoid another single catch-all commit. Commit one working change at a time—for example, a code correction, its test, then the README update. Check each staged change with `git diff --staged` before writing the message.

## 8. Basic error handling and input validation

- Your separate test file executed successfully. Its assertion-style checks cover record validation, the accepted/rejected partition and the oak summary.
- **Review what your tests demonstrate.** The tests are top-level assertions; their successful exit does not show that every important case is covered. Map them to the released validation rules and boundary cases. Where a rule lacks a check, add a small example with an explicit expected outcome. No output discrepancy was identified here, so there is no specific incorrect result to repair.
- Review your root README for accurate purpose, run and test instructions, and check that generated results are ignored rather than committed.

## 9. Problem-solving approach and method implementation

- Your code shows a clear connected workflow: `main()` calls `load_records()`, passes the rows to `process_records()`, which uses `validate_record()` and returns `(clean_records, issues)`. The cleaned records feed `summarise_oaks()`, and three `write_csv()` calls produce the outputs. The route from input to outputs is clear.
- Before final submission, make this check visible in your repository. In `code/test_silwood_trees.py`, add or refine a small assertion-based test with one valid and one invalid record. Check that `process_records()` places them in the cleaned and issues collections respectively. Then pass the returned cleaned collection to `summarise_oaks()` and check that the invalid record does not contribute. Briefly explain this flow in your root README.
