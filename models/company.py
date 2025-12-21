from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class Company:
    """
    Represents a Ukrainian company from the firms.csv dataset.

    Attributes:
        tax_id: Company tax ID (EDRPOU) - stored as string to preserve leading zeros
        name: Full official name of the company
        kved: Primary economic activity code (KVED)
        opf_code: Organizational-legal form code
        katottg: Administrative-territorial unit code
        region_code: Region (oblast) code
        local_code: Local administrative unit code
    """
    tax_id: str
    name: str
    kved: str
    opf_code: str
    katottg: str
    region_code: str
    local_code: str

    @classmethod
    def from_series(cls, series: pd.Series) -> 'Company':
        """
        Create a Company instance from a pandas Series (DataFrame row).

        Args:
            series: A pandas Series containing company data

        Returns:
            Company instance

        Raises:
            ValueError: If required fields are missing
        """
        try:
            return cls(
                tax_id=str(series['tax_id']).strip(),
                name=str(series['name']).strip(),
                kved=str(series['kved']).strip(),
                opf_code=str(series['opf_code']).strip(),
                katottg=str(series['katottg']).strip(),
                region_code=str(series['region_code']).strip(),
                local_code=str(series['local_code']).strip()
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in company data: {e}")

    @classmethod
    def from_dict(cls, data: dict) -> 'Company':
        """
        Create a Company instance from a dictionary.

        Args:
            data: Dictionary containing company data

        Returns:
            Company instance
        """
        return cls(
            tax_id=str(data.get('tax_id', '')).strip(),
            name=str(data.get('name', '')).strip(),
            kved=str(data.get('kved', '')).strip(),
            opf_code=str(data.get('opf_code', '')).strip(),
            katottg=str(data.get('katottg', '')).strip(),
            region_code=str(data.get('region_code', '')).strip(),
            local_code=str(data.get('local_code', '')).strip()
        )

    def to_dict(self) -> dict:
        """
        Convert Company instance to dictionary.

        Returns:
            Dictionary representation of the company
        """
        return {
            'tax_id': self.tax_id,
            'name': self.name,
            'kved': self.kved,
            'opf_code': self.opf_code,
            'katottg': self.katottg,
            'region_code': self.region_code,
            'local_code': self.local_code
        }

    def __str__(self) -> str:
        """String representation of the company."""
        return f"Company(tax_id={self.tax_id}, name={self.name})"

