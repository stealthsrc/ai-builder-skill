# Python Builder

Use this reference for maintainable data workflows, reporting, and cross-file automation.

## Build Safely

- Prefer the standard library unless a third-party package clearly reduces complexity.
- Use `pathlib` for paths and avoid hard-coded user-specific locations when parameters will do.
- Write transformed output to a new file by default.
- Keep dependencies explicit and minimal.

## Structure The Script

- Use a visible configuration block or `argparse` for inputs and outputs.
- Split parsing, transformation, and writing into small functions when the script is more than a short one-off.
- Include `if __name__ == "__main__":` in runnable scripts.
- Add concise comments only where the flow is not obvious.

## Tell The User How To Run It

- State where to save the file, usually as `.py`.
- Provide the exact command to run, such as `python script.py`.
- If packages are required, include the exact install command.
- Mention the Python version only when the code depends on it.

## Validate And Protect Data

- Recommend testing on a copy or a small sample input first.
- Explain the expected output files, folders, or report shape.
- Call out common issues such as missing columns, encoding problems, locked Excel files, or absent dependencies.
- Prefer readable console output so the user can verify progress quickly.
