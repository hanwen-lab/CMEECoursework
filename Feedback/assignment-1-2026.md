# Assignment 1 feedback - Hanwen Guo

**Formative feedback | Rubric 2026.2**

The converter sources have useful argument/file checks, quoted paths and conversion-status handling. Your Unix notes also recognise why the header is excluded and why sequence lines are joined. The next revision should make the commands do exactly what those explanations describe.

First correct the Unix paths for the required code/ starting directory. Q1-Q2 did not run successfully there, and Q3-Q4 returned incorrect counts. Q4 has another, separate issue: it searches ATCG, while the task asks for ATGC. Those are different motifs. Q5 counts the canonical bases together and prints a symbolic formula; it does not supply separate AT and GC counts to a ratio calculation, so no ratio was verified.

Both converters write through ../results and therefore have the opposite starting-directory assumption to the Unix answers. Align the converters with repository-root execution, preserving their useful validation, and explicitly handle a failure to create the output directory. Add your own TSV with an empty field and check the converted contents.

The README needs more than practice-repository headings. Give someone else the actual commands, expected output locations, test observations, dependencies and any help used. Ignore generated results and use more specific commit subjects than coursework or test. A useful next check is to close the terminal, start a fresh shell in the stated directory and see whether each example works without remembering how you got there.

---

## Project structure

Relevant tracked layout (simplified; missing required paths are marked):

```text
README.md
.gitignore
code/  unixPrac1.txt, tabtocsv.sh, csvtospace.sh
data/fasta/  3 required files present
data/temperatures/  4 required files present
data/tab-example.tsv [missing]
results/  no files tracked; generated on run
sandbox/  1 files tracked
```

The root README, ignore file, assessed code and supplied inputs are present. The own TSV is missing, and a file is tracked under sandbox/. No results are tracked, but the ignore file covers only temporary filename patterns.

Add data/tab-example.tsv and rules for generated results and disposable sandbox files. Preserve any durable source currently used for practice by placing it in code/ with a meaningful name. The README should explain the existing root layout with real commands rather than leaving it as a collection of headings.

**Assessed snapshot:** `34c63d6adccb8c05a7f24c9898b7dd5afb822795`
