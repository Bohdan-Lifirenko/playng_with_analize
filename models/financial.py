from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
import pandas as pd


@dataclass
class FinancialRecord:
    """
    Represents a financial indicator record from fin_values.csv dataset.

    Attributes:
        tax_id: Company tax ID (EDRPOU) - stored as string to preserve leading zeros
        my_date: Financial reporting date (end of reporting period)
        code: Financial indicator code (e.g., 2000 for revenue, 1300 for assets)
        value: Value of the financial indicator
        c_doc_sub: Reporting form type (e.g., Form 1, Form 2)
    """
    tax_id: str
    my_date: datetime
    code: int
    value: float
    c_doc_sub: str

    @classmethod
    def from_series(cls, series: pd.Series) -> 'FinancialRecord':
        """
        Create a FinancialRecord instance from a pandas Series (DataFrame row).

        Args:
            series: A pandas Series containing financial record data

        Returns:
            FinancialRecord instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        try:
            my_date = series['my_date']
            if not isinstance(my_date, datetime):
                my_date = pd.to_datetime(my_date)

            return cls(
                tax_id=str(series['tax_id']).strip(),
                my_date=my_date,
                code=int(series['code']),
                value=float(series['value']),
                c_doc_sub=str(series['c_doc_sub']).strip()
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in financial record: {e}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid data type in financial record: {e}")

    @classmethod
    def from_dict(cls, data: dict) -> 'FinancialRecord':
        """
        Create a FinancialRecord instance from a dictionary.

        Args:
            data: Dictionary containing financial record data

        Returns:
            FinancialRecord instance
        """
        my_date = data.get('my_date')
        if isinstance(my_date, str):
            my_date = pd.to_datetime(my_date)
        elif not isinstance(my_date, datetime):
            my_date = datetime.now()

        return cls(
            tax_id=str(data.get('tax_id', '')).strip(),
            my_date=my_date,
            code=int(data.get('code', 0)),
            value=float(data.get('value', 0.0)),
            c_doc_sub=str(data.get('c_doc_sub', '')).strip()
        )

    def to_dict(self) -> dict:
        """
        Convert FinancialRecord instance to dictionary.

        Returns:
            Dictionary representation of the financial record
        """
        return {
            'tax_id': self.tax_id,
            'my_date': self.my_date.strftime('%Y-%m-%d'),
            'code': self.code,
            'value': self.value,
            'c_doc_sub': self.c_doc_sub
        }

    def format_date(self, date_format: str = '%Y-%m-%d') -> str:
        """
        Format the date as a string.

        Args:
            date_format: Desired date format (default: YYYY-MM-DD)

        Returns:
            Formatted date string
        """
        return self.my_date.strftime(date_format)

    def format_value(self, decimals: int = 2, thousands_sep: str = ',') -> str:
        """
        Format the value with proper separators and decimals.

        Args:
            decimals: Number of decimal places (default: 2)
            thousands_sep: Thousands separator (default: ',')

        Returns:
            Formatted value string
        """
        return f"{self.value:,.{decimals}f}".replace(',', thousands_sep)

    def __str__(self) -> str:
        """String representation of the financial record."""
        return f"FinancialRecord(tax_id={self.tax_id}, date={self.format_date()}, code={self.code}, value={self.value})"

