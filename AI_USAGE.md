# AI Usage

## Tool and Scope

I used OpenAI ChatGPT (GPT-6.1 Sol) to help develop, understand, test, and document my Lab 5 Snakemake workflow.

## Prompts

1. Converting Lab 3 & Lab 4 Scripts into Workflow Steps
"I am working on a Health Data Science lab where I need to turn my standalone scripts from previous assignments into a scalable, automated pipeline. Here are the scripts I used in Lab 3 and Lab 4 under /Users/jiahetian/Desktop/GWU Y3 S1/PUBH 6854 Applied Computing. Can you help me break these down into logical, modular workflow steps? For each step, clearly identify what the exact input files are, what parameters or scripts are being executed, and what the expected output files should be so that each step connects cleanly into the next."

2. Learning Snakemake Syntax & Writing the Snakefile

"I am new to Snakemake and need to build a Snakefile to automate a bioinformatics/health data science pipeline. Based on the workflow steps we just mapped out [or paste your script details here], please write a clean, well-commented Snakefile for me. Make sure to include a rule all at the top that defines the final target outputs, and use wildcards or config.yaml where it makes sense to keep things scalable. As you write the rules (input, output, shell/script), briefly explain the Snakemake syntax choices you made so I can learn how the DAG (Directed Acyclic Graph) connects everything together."

Error (?):
Sankefile has multiple lines highlighted in red, which I thought were errors. But after confirming with GPT, it's caused by VS Code, not errors.

3. Debugging, Clean Full Run & Partial Re-run Validation

Part A: Clean Full Run & Debugging

"I am about to run my Snakemake workflow from scratch. First, give me the exact terminal commands to do a dry-run (-n), visualize the DAG, clean up any old output files, and execute a fresh, full run while saving the terminal execution logs to a file for my submission. Also, if I hit any errors, like MissingInputException or RuleException, act as my debugging partner and tell me what to check first."

Part B: Partial Re-run Validation Experiment

"To prove my Snakemake pipeline actually tracks dependencies properly, I need to design a 'partial re-run' validation experiment and save the proof. Suggest a realistic modification I can make to just one intermediate file, parameter, or script in the middle of my pipeline. Walk me through the exact commands to run Snakemake afterward so that it only re-executes the downstream rules affected by my change, and show me how to save the dry-run/execution output to prove the upstream steps were skipped."

4. Generating and Polishing Final README.md

"I have finished building and testing my Snakemake workflow, and now I need to write a clear, professional README.md for my GitHub repository. Below are my Snakefile, the directory structure of my project, and the results from my full run and partial re-run tests Users/jiahetian/Desktop/GWU Y3 S1/PUBH 6854 Applied Computing/... Please draft a well-structured README.md that includes:A brief overview of the pipeline's purpose and biological/health data context; Prerequisites and setup instructions (e.g., Conda environment); A clear explanation of the workflow steps (referencing my DAG diagram); Step-by-step instructions on how to reproduce the clean full run.A summary of my partial re-run experiment demonstrating pipeline efficiency. Keep the tone clear, concise, and academic, avoiding overly robotic or buzzword-heavy phrasing."