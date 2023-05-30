import json
import time
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Generic, ParamSpec, TypeVar

import aiofiles
from humps import camelize
from pydantic import BaseModel
from rich import print

from td.config import TdConfiguration

config = TdConfiguration()


P = ParamSpec("P")
R = TypeVar("R")


class QueryInitializer(Generic[P, R]):
    """
    Decorator class for initializing pydantic query objects.

    This decorator serves as a flexible initializer for a query object. It accepts
    arguments in one of the following forms:

    1. A named arguments representation (parameter_name=..., other_param=...)
    2. A dictionary representation {"parameter_name": ..., "other_param":...}
    3. An instance of a Pydantic Model

    Args:
        query_class (Callable[P, R]): The pydantic query class to be instantiated.

    Usage:

    @QueryInitializer(query_class)
    def function_name(self, query_instance):
        pass
    """

    def __init__(self, query_class: Callable[P, R]):
        self.query_class = query_class

    def __call__(self, func: Callable):
        query_class = self.query_class

        def inner_wrapper(self, *args, **kwargs):
            """
            Inner wrapper function that creates an instance of query_class based
            on the provided arguments. If the first argument is already an instance
            of query_class, it uses that. If the first argument is a dictionary,
            it unpacks it to create an instance of query_class. Else, it uses the
            provided arguments to instantiate query_class.

            Args:
                self: The instance of the enclosing class.
                *args: The positional arguments.
                **kwargs: The keyword arguments.

            Returns:
                The result of calling the decorated function with the instance of query_class.
            """
            inner_wrapper.__doc__ = func.__doc__
            # Check if the first argument is already an instance of query_class
            if len(args) > 0 and isinstance(args[0], query_class):
                query_instance = args[0]
            elif len(args) > 0 and isinstance(args[0], dict):
                query_instance = query_class(**args[0])
            else:
                # Instantiate the query_class with the arguments
                query_instance = query_class(*args, **kwargs)

            # Call the function with the instance
            return func(self, query_instance)

        return inner_wrapper


# Custom conversion function to convert Pydantic objects to JSON-compatible types
def convert_to_json(obj):
    if isinstance(obj, BaseModel):
        return obj.dict()
    return obj


# Function to convert python dictionary to JSON
def dict_to_json(input_dict):
    json_dict = {key: convert_to_json(value) for key, value in input_dict.items()}
    return json.dumps(json_dict, default=lambda o: o.__dict__)


def to_camel(string: str) -> str:
    """
    Converts a snake_case string to camelCase.

    Parameters:
    string (str): The string to convert to camelCase.

    Returns:
    str: The input string in camelCase.

    Example:
    >>> to_camel('hello_world')
    'helloWorld'
    """
    return camelize(string)


def is_valid_iso_date_str(date_str: str) -> bool:
    """
    Check if a string is a valid ISO or YYYY-MM-DD date string

    ("%Y-%m-%dT%H:%M:%S" or "%Y-%m-%d")
    """
    formats = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]

    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue

    return False


def is_unix_time(unix_time_ms):
    """
    Checks whether a given integer represents a Unix time in milliseconds.

    Parameters:
    unix_time_ms (int): The integer to check.

    Returns:
    bool: True if the input value represents a valid Unix time in milliseconds, False otherwise.

    Example:
    >>> is_unix_time(1633305852000)
    True
    >>> is_unix_time(2000000000000)
    False
    """
    current_unix_time = int(time.time()) * 1000  # Convert to ms
    return unix_time_ms >= 0 and unix_time_ms < current_unix_time


def convert_to_unix_time_ms(time_to_convert: int | date | datetime):
    """
    Converts a date or datetime object or Unix time in milliseconds to Unix time in milliseconds.

    Parameters:
    time_to_convert (int | date | datetime): The time to convert. If an integer, it is assumed to represent Unix time in milliseconds.

    Returns:
    int: The Unix time in milliseconds.

    Raises:
    ValueError: If the input value is not a supported time format or is not a valid Unix time.
    """
    if isinstance(time_to_convert, int):
        if is_unix_time(time_to_convert):
            # Input value is already in Unix time format
            return time_to_convert
        else:
            raise ValueError("Input value is not a Unix time")

    # Handle dates and datetimes
    if isinstance(time_to_convert, datetime):
        return int(time_to_convert.timestamp() * 1000)
    elif isinstance(time_to_convert, date):
        return int(
            datetime.strptime(time_to_convert.isoformat(), "%Y-%m-%d").timestamp()
            * 1000
        )

    # If it's not a supported type, raise an error
    raise ValueError("Unsupported time format")


# async def save_raw_json(raw_json, timeframe, symbol):
#     # raw_json = pydantic_object.dict(by_alias=True)
#     today = datetime.today()
#     day, month, year = str(today.day), str(today.month), str(today.year)
#     datepath = Path()/year/month/day
#     symbol_processed = symbol.replace("/", "")
#     base_directory = tda_futures_base_path/timeframe/symbol_processed
#     filename = Path(symbol_processed + "-" + year + "-" + month  + "-" +  day + ".json")
#     path = base_directory/datepath/filename
#     path.parent.mkdir(parents=True, exist_ok=True)
#     print(f"Received data for {symbol}, saving it to: {path}")

#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(raw_json, f)


def default_futures_file_path(symbol, timeframe):
    try:
        tda_futures_base_path = Path(config.data_paths.futures_data_base_path)
    except AttributeError:
        import inspect

        caller_path = (
            Path(inspect.getframeinfo(inspect.currentframe()).filename).resolve().parent
        )
        tda_futures_base_path = caller_path

    today = datetime.today()
    day, month, year = str(today.day), str(today.month), str(today.year)
    datepath = Path() / year / month / day

    symbol_processed = symbol.replace("/", "")
    base_directory = tda_futures_base_path / timeframe / symbol_processed
    filename = Path(symbol_processed + "-" + year + "-" + month + "-" + day + ".json")
    path = base_directory / datepath / filename

    return path


async def save_raw_json(raw_json: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving data to: {path}")

    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(raw_json))
