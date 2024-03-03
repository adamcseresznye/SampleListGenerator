import ast
import os

import click
import numpy as np
import pandas as pd


class SampleListGenerator:
    """
    A class used to create a list of samples from a given CSV file.

    Attributes
    ----------
    location : str
        The location of the CSV file.
    start : int
        The starting index for the location column in the dataframe.
    sample_names : list
        The list of sample names read from the CSV file.
    dataframe : pandas.DataFrame
        The dataframe created from the sample names and their locations.
    count_dict : dict
        A dictionary to keep track of the count of duplicated sample names.

    Methods
    -------
    create_dataframe():
        Creates a dataframe from the sample names and their locations.
    increment_duplicated_names(sample: str) -> str:
        Increments the count of duplicated sample names in the count_dict.
    return_sample_list(target_dict: dict, randomize: bool = True) -> pandas.DataFrame:
        Returns a sample list with duplicated sample names incremented and optionally randomized.
    """

    def __init__(self, location: str, start: int = 1):
        if not os.path.exists(location):
            raise ValueError(
                f"The file at location {location} does not exist. Please provide a valid file location."
            )
        self.location = location
        self.sample_names = pd.read_csv(self.location, header=None).squeeze().tolist()
        self.start = start
        self.dataframe = self.create_dataframe()
        self.count_dict = {}

    def create_dataframe(self) -> pd.DataFrame:
        """
        Creates a dataframe from the sample names and their locations.

        Returns:
            pandas.DataFrame: The created dataframe.
        """
        df = pd.DataFrame(
            {
                "sample": self.sample_names,
                "location": [
                    i for i in range(self.start, self.start + len(self.sample_names))
                ],
            }
        )
        return df

    def increment_duplicated_names(self, sample: str) -> str:
        """
        Increments the count of duplicated sample names in the count_dict.

        Parameters:
            sample (str): The sample name to increment.

        Returns:
            str: The incremented sample name.
        """
        if sample in self.count_dict:
            self.count_dict[sample] += 1
            if self.count_dict[sample] > 1:
                return sample + "_" + str(self.count_dict[sample])

        else:
            self.count_dict[sample] = 1
        return sample

    def return_sample_list(
        self, target_dict: dict, randomize: bool = True
    ) -> pd.DataFrame:
        """
        Returns a sample list with duplicated sample names incremented and optionally randomized.

        Parameters:
            target_dict (dict): A dictionary with target sample names and their repeat counts.
            randomize (bool): Whether to randomize the sample list. Defaults to True.

        Returns:
            pandas.DataFrame: The sample list as a dataframe.
        """
        if target_dict is None:
            return self.dataframe
        conditions = []
        choices = []
        for target_name, repeat_count in target_dict.items():
            conditions.append(self.dataframe["sample"].isin([target_name]))
            choices.append(repeat_count)

        dataframe_with_duplicates = self.dataframe.iloc[
            self.dataframe.index.repeat(
                np.select(
                    condlist=conditions,
                    choicelist=choices,
                    default=1,
                )
            )
        ].reset_index(drop=True)

        dataframe_with_duplicates["sample"] = dataframe_with_duplicates["sample"].apply(
            self.increment_duplicated_names
        )

        if randomize:
            return dataframe_with_duplicates.sample(frac=1)
        else:
            return dataframe_with_duplicates


@click.command()
@click.option(
    "--location",
    help='The location of the txt file with sample names. For example: "sample_names.txt"',
)
@click.option(
    "--target_dict",
    default=None,
    help='A Python dictionary with target sample names and their repeat counts if multiple injections are desired. For example: {"sample1": 2, "sample2": 3}. Defaults to None.',
)
@click.option(
    "--start",
    default=1,
    help="The starting index for the first sample on the sample tray. Defaults to 1.",
)
@click.option(
    "--randomize",
    default=True,
    help="Whether to randomize the sample list. Defaults to True.",
)
@click.option(
    "--export",
    default=True,
    help="Whether to export the resulting sample list as csv. Defaults to True.",
)
def main(location, target_dict, start, randomize, export):
    """A program that generates sample list with vial locations from given sample names."""
    target_dict = ast.literal_eval(target_dict)
    creator = SampleListGenerator(location=location, start=start)
    injection_sequence = creator.return_sample_list(
        target_dict=target_dict, randomize=randomize
    )

    if export:
        file_path = "sample_list_result.csv"
        injection_sequence.to_csv(file_path, index=False)
        click.echo(f"The sample list was exported to {file_path}")

    click.echo(injection_sequence)


if __name__ == "__main__":
    main()
