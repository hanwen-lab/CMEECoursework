# Assignment 3 formative feedback

This feedback is organised using the [Computing Bootcamp rubric](https://mulquabio.github.io/MQB/rubrics/Computing_Bootcamp_Rubric.html). It does not award a mark; use it to decide what to revise and check before final submission.

## Criterion 1: Repository organisation & workflow discipline

Before final submission, check that the required scripts are under `code/`, supplied inputs are under `data/`, and generated files remain outside Git.

## Criterion 2: Code completeness & functional correctness

- The fixed tree-height program ran successfully, and `results/TreeHts.csv` satisfied the checked required output format and values on both attempts. Your code also shows a clearly named function, degree-to-radian conversion and checks before writing results.
- Before final submission, **Complete the generalised tree-height route.** Its normal run did not produce `results/trees_treeheights.csv`. Your code shows a remaining `browser()` call before calculation and output, while `code/run_get_TreeHeight.sh` is empty. Remove the debugging interruption and implement the required wrapper so it invokes the generalised program with the supplied input argument. Test the R program and wrapper separately: test both the R program and its shell wrapper separately from the fixed program.

## Criterion 3: Code quality & style

As you revise, keep names descriptive, use comments to explain decisions rather than restating code, and avoid repeating the same calculation in several places.

## Criterion 4: Documentation

- Your required project paths and supplied datasets are present. The supplied data match the original inputs, and the root README documents the fixed tree-height command, input and output.
- Your README includes a simple independent height example. This gives you a useful basis for checking the route from measurements to calculated heights, although the evidence does not show that you performed that comparison.
- Before final submission, **Extend the README to cover the complete workflow.** It currently documents only the fixed Assignment 3 route. Add purpose, commands, inputs, outputs and small test examples for the generalised program, wrapper and Pound Hill analysis. Record your independent height comparison and briefly explain what the Pound Hill summaries and plots represent. Recent task-specific Git messages are useful; continue using these rather than vague messages such as `test`.

## Criterion 5: Version-control practice

Commit each functional revision with a short message that says what changed; this makes your development easier to follow than one large final commit.

## Criterion 8: Basic error-handling & input validation

- The invalid-input runs stopped with distance/finite-value messages and the expected no-output behaviour. These are useful checks, but do not establish that every invalid input is handled correctly.

## Criterion 9: Problem-solving approach & method implementation

- Before final submission, **Check the Pound Hill data orientation before summarising.** In your code, species occupy rows and quadrats occupy columns, but species names are assigned as column names; the reported species and quadrat dimensions are also reversed. This risks stopping the analysis or misinterpreting its summaries. Inspect `dim(species_counts)`, compare it with the species-name and sampling-information lengths, and trace one species and one quadrat through the table. Then manually check one quadrat’s richness and abundance and one plot’s mean. Ensure the script creates `results/` before writing to it.
- Before final submission, **Make generated outputs reproducible rather than relying on committed files.** `results/pound_hill_plot_richness.pdf` is tracked, while `.gitignore` excludes only results CSVs. Stop tracking the generated PDF and extend the ignore rule appropriately. The Pound Hill run was flagged for review because that PDF was already committed; its newly generated CSV and PDF were not collected. This is not evidence that those outputs are incorrect or absent from your repository. Regenerate and verify the exact required paths, `results/pound_hill_plot_richness.csv` and `results/pound_hill_plot_richness.pdf`, comparing them with the filenames your script creates. Open the PDF to check labels, values and biological meaning; no newly generated figure was available for visual review.

## Criterion 10: Learning progression demonstration

Use this feedback as a revision checklist. Make the changes in small, descriptive commits, then add a short README note explaining what you changed and how you checked it. This will make your development from this formative checkpoint visible in the final portfolio.

## Priorities before final submission

- Run commands from the project directory containing `code/`, `data/` and the root `README.md`. After the fixes, rerun one ordinary and one invalid case for each tree-height route. Check stderr as well as whether execution stops, and confirm invalid cases do not create a new result. Finally, regenerate the Pound Hill outputs without relying on existing results, inspect the table and PDF, and commit the code and documentation changes rather than generated files.
