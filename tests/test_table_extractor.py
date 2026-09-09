from src.table_extractor import (
    table_to_text
)


def test_table_to_text():

    table = [

        ["Name", "Age", "City"],

        ["Prathamesh", "22", "Pune"],

        ["Rahul", "25", "Mumbai"]

    ]


    result = table_to_text(
        table
    )


    assert (
        "Name | Age | City"
        in result
    )


    assert (
        "Prathamesh | 22 | Pune"
        in result
    )


def test_empty_table():

    table = []


    result = table_to_text(
        table
    )


    assert result == ""


def test_table_with_none_values():

    table = [

        ["Name", "Salary"],

        ["John", None]

    ]


    result = table_to_text(
        table
    )


    assert (
        "John |"
        in result
    )