import pandas as pd
from typing import Optional, List
import os
from pathlib import Path


class DataLoader:
    """
    Service for loading and caching CSV data files.

    Handles loading of firms.csv and fin_values.csv with proper data types
    and implements in-memory caching to avoid reloading on every request.
    """

    def __init__(self):
        self.firms_df: Optional[pd.DataFrame] = None
        self.fin_values_df: Optional[pd.DataFrame] = None
        self._is_loaded: bool = False

    def load_data(self, firms_path: str, fin_values_path: str) -> None:
        """
        Load CSV data files into memory with proper dtype handling.

        Args:
            firms_path: Path to firms.csv file
            fin_values_path: Path to fin_values.csv file

        Raises:
            FileNotFoundError: If CSV files are not found
            ValueError: If required columns are missing
            Exception: For other loading errors
        """
        try:
            # Validate files exist
            if not os.path.exists(firms_path):
                raise FileNotFoundError(f"Firms file not found: {firms_path}")
            if not os.path.exists(fin_values_path):
                raise FileNotFoundError(f"Financial values file not found: {fin_values_path}")

            # Load firms.csv
            print(f"Loading firms data from: {firms_path}")
            self.firms_df = pd.read_csv(
                firms_path,
                dtype={
                    'tax_id': str,      # Preserve leading zeros in EDRPOU
                    'name': str,
                    'kved': str,
                    'opf_code': str,
                    'katottg': str,
                    'region_code': str,
                    'local_code': str
                }
            )

            # Validate firms columns
            required_firms_cols = ['tax_id', 'name', 'kved', 'opf_code',
                                   'katottg', 'region_code', 'local_code']
            missing_cols = set(required_firms_cols) - set(self.firms_df.columns)
            if missing_cols:
                raise ValueError(f"Missing required columns in firms.csv: {missing_cols}")

            # Strip whitespace from tax_id for consistent lookups
            self.firms_df['tax_id'] = self.firms_df['tax_id'].str.strip()

            print(f"Loaded {len(self.firms_df)} companies")

            # Load fin_values.csv
            print(f"Loading financial data from: {fin_values_path}")
            self.fin_values_df = pd.read_csv(
                fin_values_path,
                dtype={
                    'tax_id': str,      # Preserve leading zeros in EDRPOU
                    'code': int,
                    'value': float,
                    'c_doc_sub': str
                },
                parse_dates=['my_date']  # Parse date column automatically
            )

            # Validate fin_values columns
            required_fin_cols = ['tax_id', 'my_date', 'code', 'value', 'c_doc_sub']
            missing_cols = set(required_fin_cols) - set(self.fin_values_df.columns)
            if missing_cols:
                raise ValueError(f"Missing required columns in fin_values.csv: {missing_cols}")

            # Strip whitespace from tax_id for consistent lookups
            self.fin_values_df['tax_id'] = self.fin_values_df['tax_id'].str.strip()

            # Sort by date for better performance
            self.fin_values_df = self.fin_values_df.sort_values(['tax_id', 'my_date'])

            print(f"Loaded {len(self.fin_values_df)} financial records")

            self._is_loaded = True
            print("Data loading completed successfully")

        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise
        except ValueError as e:
            print(f"Data validation error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error loading data: {e}")
            raise

    def is_loaded(self) -> bool:
        """
        Check if data has been loaded.

        Returns:
            True if data is loaded, False otherwise
        """
        return self._is_loaded and self.firms_df is not None and self.fin_values_df is not None

    def get_company_data(self, tax_id: str) -> Optional[pd.Series]:
        """
        Get company data by tax_id.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            pandas Series with company data or None if not found
        """
        if not self.is_loaded():
            raise RuntimeError("Data not loaded. Call load_data() first.")

        tax_id = str(tax_id).strip()
        result = self.firms_df[self.firms_df['tax_id'] == tax_id]

        if result.empty:
            return None

        return result.iloc[0]

    def get_financial_data(self, tax_id: str) -> pd.DataFrame:
        """
        Get all financial records for a company.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            DataFrame with financial records (empty if none found)
        """
        if not self.is_loaded():
            raise RuntimeError("Data not loaded. Call load_data() first.")

        tax_id = str(tax_id).strip()
        return self.fin_values_df[self.fin_values_df['tax_id'] == tax_id].copy()

    def get_financial_data_by_code(self, tax_id: str, code: int) -> pd.DataFrame:
        """
        Get financial records for a company filtered by indicator code.

        Args:
            tax_id: Company tax ID (EDRPOU)
            code: Financial indicator code (e.g., 2000 for revenue)

        Returns:
            DataFrame with filtered financial records
        """
        if not self.is_loaded():
            raise RuntimeError("Data not loaded. Call load_data() first.")

        tax_id = str(tax_id).strip()
        return self.fin_values_df[
            (self.fin_values_df['tax_id'] == tax_id) &
            (self.fin_values_df['code'] == code)
        ].copy()

    def get_financial_data_by_date(self, tax_id: str, date: str) -> pd.DataFrame:
        """
        Get financial records for a company for a specific date.

        Args:
            tax_id: Company tax ID (EDRPOU)
            date: Date string (will be parsed to datetime)

        Returns:
            DataFrame with financial records for the specified date
        """
        if not self.is_loaded():
            raise RuntimeError("Data not loaded. Call load_data() first.")

        tax_id = str(tax_id).strip()
        target_date = pd.to_datetime(date)

        return self.fin_values_df[
            (self.fin_values_df['tax_id'] == tax_id) &
            (self.fin_values_df['my_date'] == target_date)
        ].copy()

    def get_available_dates(self, tax_id: str) -> List[str]:
        """
        Get all available reporting dates for a company.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            List of date strings in 'YYYY-MM-DD' format, sorted newest first
        """
        if not self.is_loaded():
            raise RuntimeError("Data not loaded. Call load_data() first.")

        tax_id = str(tax_id).strip()
        company_data = self.fin_values_df[self.fin_values_df['tax_id'] == tax_id]

        if company_data.empty:
            return []

        # Get unique dates, sort descending (newest first)
        dates = company_data['my_date'].unique()
        dates = sorted(dates, reverse=True)

        # Convert to string format
        return [pd.Timestamp(date).strftime('%Y-%m-%d') for date in dates]

    def company_exists(self, tax_id: str) -> bool:
        """
        Check if a company exists in the dataset.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            True if company exists, False otherwise
        """
        if not self.is_loaded():
            raise RuntimeError("Data not loaded. Call load_data() first.")

        tax_id = str(tax_id).strip()
        return not self.firms_df[self.firms_df['tax_id'] == tax_id].empty

    def get_stats(self) -> dict:
        """
        Get statistics about loaded data.

        Returns:
            Dictionary with data statistics
        """
        if not self.is_loaded():
            return {
                'loaded': False,
                'companies_count': 0,
                'financial_records_count': 0
            }

        return {
            'loaded': True,
            'companies_count': len(self.firms_df),
            'financial_records_count': len(self.fin_values_df),
            'unique_companies_with_data': self.fin_values_df['tax_id'].nunique(),
            'date_range': {
                'earliest': self.fin_values_df['my_date'].min().strftime('%Y-%m-%d'),
                'latest': self.fin_values_df['my_date'].max().strftime('%Y-%m-%d')
            } if not self.fin_values_df.empty else None
        }

    def reload_data(self, firms_path: str, fin_values_path: str) -> None:
        """
        Reload data from CSV files (clears cache and reloads).

        Args:
            firms_path: Path to firms.csv file
            fin_values_path: Path to fin_values.csv file
        """
        print("Reloading data...")
        self.firms_df = None
        self.fin_values_df = None
        self._is_loaded = False
        self.load_data(firms_path, fin_values_path)

