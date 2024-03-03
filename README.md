**Sample list generator**

```
  A program that generates sample list with vial locations from given sample
  names.

Options:
  --location TEXT      The location of the txt file with sample names. For
                       example: "sample_names.txt"
  --target_dict TEXT   A Python dictionary with target sample names and their
                       repeat counts if multiple injections are desired. For
                       example: {"sample1": 2, "sample2": 3}. Defaults to
                       None.
  --start INTEGER      The starting index for the first sample on the sample
                       tray. Defaults to 1.
  --randomize BOOLEAN  Whether to randomize the sample list. Defaults to True.
  --export BOOLEAN     Whether to export the resulting sample list as csv.
                       Defaults to True.
  --help               Show this message and exit.

```

**Example usage as CLI**
python sample_list_generator.py --location="example.txt" --target_dict="{'qc':5, 'blank': 3}" --start=10 --randomize=False --export=False

**Example usage as a Python module**

```python
import sample_list_generator

target_dict = {"blank": 3, "qc": 3, "isrs": 5}
target_dict = None
location = "example.txt"

# Create an instance of SampleListGenerator
creator = sample_list_generator.SampleListGenerator(location)

# Call the 'return_sample_list' method on the instance and print the result
result = creator.return_sample_list(target_dict, randomize=False)
print(result)
```
