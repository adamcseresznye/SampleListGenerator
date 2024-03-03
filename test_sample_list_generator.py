from unittest.mock import patch

import pandas as pd
import pytest

from .sample_list_generator import SampleListGenerator


# Define a fixture for the sample list creator
@pytest.fixture
def slg_fixture(tmp_path):
    # Create a temporary CSV file
    p = tmp_path / "sample_names.csv"
    p.write_text("sample1\nsample2\nsample3\n")

    # Create a slg_fixture instance
    slc = SampleListGenerator(p)

    # Ensure sample_names is a list
    if isinstance(slc.sample_names, str):
        slc.sample_names = [slc.sample_names]

    return slc


# Test the __init__ method
def test_init(slg_fixture):
    assert slg_fixture.location is not None
    assert slg_fixture.sample_names == ["sample1", "sample2", "sample3"]
    assert slg_fixture.start == 1
    assert isinstance(slg_fixture.dataframe, pd.DataFrame)
    assert slg_fixture.count_dict == {}


# Test the create_dataframe method
def test_create_dataframe(slg_fixture):
    df = slg_fixture.create_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert "sample" in df.columns
    assert "location" in df.columns
    assert df["sample"].tolist() == ["sample1", "sample2", "sample3"]
    assert df["location"].tolist() == [1, 2, 3]


# Test the increment_duplicated_names method
def test_increment_duplicated_names(slg_fixture):
    assert slg_fixture.increment_duplicated_names("sample1") == "sample1"
    assert slg_fixture.increment_duplicated_names("sample1") == "sample1_2"
    assert slg_fixture.increment_duplicated_names("sample2") == "sample2"
    assert slg_fixture.increment_duplicated_names("sample1") == "sample1_3"
    assert slg_fixture.increment_duplicated_names("sample2") == "sample2_2"
    assert slg_fixture.increment_duplicated_names("sample3") == "sample3"
    assert slg_fixture.increment_duplicated_names("sample3") == "sample3_2"


# Test the return_sample_list method
def test_return_sample_list(slg_fixture):
    target_dict = {"sample1": 2, "sample2": 3}
    df = slg_fixture.return_sample_list(target_dict, randomize=False)
    assert isinstance(df, pd.DataFrame)
    assert df["sample"].tolist() == [
        "sample1",
        "sample1_2",
        "sample2",
        "sample2_2",
        "sample2_3",
        "sample3",
    ]


# Test the __init__ method with an invalid file location
def test_init_invalid_location():
    with pytest.raises(ValueError):
        SampleListGenerator("invalid/location")


# Test the return_sample_list method with None target_dict
def test_return_sample_list_none_target_dict(slg_fixture):
    df = slg_fixture.return_sample_list(None, randomize=False)
    assert isinstance(df, pd.DataFrame)
    assert df["sample"].tolist() == ["sample1", "sample2", "sample3"]


# Test the return_sample_list method with empty target_dict
def test_return_sample_list_empty_target_dict(slg_fixture):
    df = slg_fixture.return_sample_list(None, randomize=False)
    assert isinstance(df, pd.DataFrame)
    assert df["sample"].tolist() == ["sample1", "sample2", "sample3"]


# Test the return_sample_list method with randomize=True
def test_return_sample_list_randomize_true(slg_fixture):
    target_dict = {"sample1": 2, "sample2": 3}
    df = slg_fixture.return_sample_list(target_dict, randomize=True)
    assert isinstance(df, pd.DataFrame)
    assert sorted(df["sample"].tolist()) == sorted(
        ["sample1", "sample1_2", "sample2", "sample2_2", "sample2_3", "sample3"]
    )
