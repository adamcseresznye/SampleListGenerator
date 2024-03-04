**Sample list generator**

```bash
  A program that generates sample list with vial locations for GC/LC-MS
  applications  from a given txt file, handling duplicate sample names, and
  optionally  exports the randomized or ordered list as a CSV file.

Options:
  --location TEXT           The location of the txt file with sample names.
                            For example: "sample_names.txt"
  --replicate_samples TEXT  A dictionary containing sample names to be
                            injected multiple times, along with their
                            corresponding repeat counts. For example:
                            {"sample1": 2, "sample2": 3}. Defaults to None.
  --start INTEGER           The starting index for the first sample on the
                            sample tray. Defaults to 1.
  --randomize BOOLEAN       Whether to randomize the sample list. Defaults to
                            True.
  --export BOOLEAN          Whether to export the resulting sample list as
                            csv. Defaults to True.
  --help                    Show this message and exit.

```
**Setup project**

```bash
# Step 1: clone repository
git clone https://github.com/adamcseresznye/SampleListGenerator.git

# Step 2: Install requirements
pip install -r requirements. txt

# Step 3: See example usage below

```

**Example usage as CLI**

```bash
python sample_list_generator.py --location="example.txt" --replicate_samples="{'qc':5, 'blank': 3}" --start=10 --randomize=False --export=False
```

**Example usage as a Python module**

```python
import sample_list_generator

replicate_samples = {"blank": 3, "qc": 3, "isrs": 5} # if some samples need to be injected repeatedly…
replicate_samples = None # If samples need to be injected only once…
location = "example.txt"

# Create an instance of SampleListGenerator
creator = sample_list_generator.SampleListGenerator(location)

# Call the 'return_sample_list' method on the instance and print the result
result = creator.return_sample_list(replicate_samples, randomize=False)
print(result)
```
