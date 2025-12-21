from typing import Optional, List, Dict
from models.company import Company
from models.financial import FinancialRecord
from services.data_loader import DataLoader


class FinancialService:
    """
    Business logic service for financial data operations.

    Provides high-level methods for retrieving and calculating financial metrics
    for Ukrainian companies. Integrates with DataLoader and data models.
    """

    # Financial indicator codes
    CODE_REVENUE = 2000      # Revenue (Form 2)
    CODE_ASSETS = 1300       # Assets (Form 1)
    CODE_EQUITY = 1495       # Equity (Form 1)

    def __init__(self, data_loader: DataLoader):
        """
        Initialize FinancialService with a DataLoader instance.

        Args:
            data_loader: DataLoader instance for data access
        """
        self.data_loader = data_loader

    def get_company_by_tax_id(self, tax_id: str) -> Optional[Company]:
        """
        Retrieve company information by tax ID.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            Company instance if found, None otherwise
        """
        company_series = self.data_loader.get_company_data(tax_id)

        if company_series is None:
            return None

        return Company.from_series(company_series)

    def get_revenue_data(self, tax_id: str) -> List[Dict]:
        """
        Get all revenue records (code 2000) for a company.

        Returns revenue data sorted by date for charting purposes.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            List of dictionaries with 'date' and 'value' keys.
            Returns empty list if no revenue data found.

        Example:
            [
                {"date": "2024-12-31", "value": 5000000.00},
                {"date": "2023-12-31", "value": 4500000.00}
            ]
        """
        revenue_df = self.data_loader.get_financial_data_by_code(
            tax_id,
            self.CODE_REVENUE
        )

        if revenue_df.empty:
            return []

        # Sort by date ascending for proper chart display
        revenue_df = revenue_df.sort_values('my_date')

        # Convert to list of dictionaries
        result = []
        for _, row in revenue_df.iterrows():
            record = FinancialRecord.from_series(row)
            result.append({
                'date': record.format_date(),
                'value': record.value
            })

        return result

    def get_balance_data(self, tax_id: str, date: str) -> Dict:
        """
        Get balance sheet data (assets, equity, liabilities) for a specific date.

        Calculates liabilities as Assets - Equity.

        Args:
            tax_id: Company tax ID (EDRPOU)
            date: Date string in 'YYYY-MM-DD' format

        Returns:
            Dictionary with 'assets', 'equity', 'liabilities' keys.
            Returns dict with None values if data not found.

        Example:
            {
                "assets": 3000000.00,
                "equity": 2000000.00,
                "liabilities": 1000000.00
            }
        """
        # Get all financial data for the specific date
        balance_df = self.data_loader.get_financial_data_by_date(tax_id, date)

        if balance_df.empty:
            return {
                'assets': None,
                'equity': None,
                'liabilities': None,
                'date': date
            }

        # Extract assets and equity
        assets_row = balance_df[balance_df['code'] == self.CODE_ASSETS]
        equity_row = balance_df[balance_df['code'] == self.CODE_EQUITY]

        assets = assets_row['value'].iloc[0] if not assets_row.empty else None
        equity = equity_row['value'].iloc[0] if not equity_row.empty else None

        # Calculate liabilities
        liabilities = None
        if assets is not None and equity is not None:
            liabilities = self.calculate_liabilities(assets, equity)

        return {
            'assets': assets,
            'equity': equity,
            'liabilities': liabilities,
            'date': date
        }

    def get_available_dates(self, tax_id: str) -> List[str]:
        """
        Get all available financial reporting dates for a company.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            List of date strings in 'YYYY-MM-DD' format, sorted newest first.
            Returns empty list if no financial data found.
        """
        return self.data_loader.get_available_dates(tax_id)

    @staticmethod
    def calculate_liabilities(assets: float, equity: float) -> float:
        """
        Calculate liabilities from assets and equity.

        Liabilities = Assets - Equity

        Args:
            assets: Total assets value
            equity: Total equity value

        Returns:
            Calculated liabilities value
        """
        return assets - equity

    def get_company_summary(self, tax_id: str) -> Optional[Dict]:
        """
        Get comprehensive company summary including basic info and latest financials.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            Dictionary with company info and latest financial data, or None if not found
        """
        company = self.get_company_by_tax_id(tax_id)

        if company is None:
            return None

        # Get available dates
        dates = self.get_available_dates(tax_id)
        latest_date = dates[0] if dates else None

        # Get latest balance data if available
        balance_data = None
        if latest_date:
            balance_data = self.get_balance_data(tax_id, latest_date)

        # Get revenue data
        revenue_data = self.get_revenue_data(tax_id)

        return {
            'company': company.to_dict(),
            'latest_date': latest_date,
            'balance': balance_data,
            'revenue_count': len(revenue_data),
            'available_dates': dates
        }

    def format_currency(self, value: Optional[float], decimals: int = 2) -> str:
        """
        Format a financial value as currency string.

        Args:
            value: Numeric value to format
            decimals: Number of decimal places (default: 2)

        Returns:
            Formatted currency string or 'N/A' if value is None
        """
        if value is None:
            return 'N/A'

        return f"{value:,.{decimals}f} UAH"

    def validate_balance_sheet(self, tax_id: str, date: str) -> Dict:
        """
        Validate balance sheet equation: Assets = Equity + Liabilities

        Args:
            tax_id: Company tax ID (EDRPOU)
            date: Date string in 'YYYY-MM-DD' format

        Returns:
            Dictionary with validation results
        """
        balance = self.get_balance_data(tax_id, date)

        if balance['assets'] is None or balance['equity'] is None:
            return {
                'valid': False,
                'reason': 'Missing data',
                'balance': balance
            }

        calculated_liabilities = balance['liabilities']
        expected_total = balance['equity'] + calculated_liabilities

        # Allow for small floating point differences
        is_valid = abs(balance['assets'] - expected_total) < 0.01

        return {
            'valid': is_valid,
            'assets': balance['assets'],
            'equity': balance['equity'],
            'liabilities': calculated_liabilities,
            'difference': balance['assets'] - expected_total,
            'date': date
        }

    def get_revenue_growth(self, tax_id: str) -> Optional[Dict]:
        """
        Calculate revenue growth statistics.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            Dictionary with growth statistics or None if insufficient data
        """
        revenue_data = self.get_revenue_data(tax_id)

        if len(revenue_data) < 2:
            return None

        # Sort by date ascending
        sorted_data = sorted(revenue_data, key=lambda x: x['date'])

        latest = sorted_data[-1]['value']
        previous = sorted_data[-2]['value']

        growth_amount = latest - previous
        growth_percent = (growth_amount / previous * 100) if previous != 0 else 0

        return {
            'latest_revenue': latest,
            'previous_revenue': previous,
            'growth_amount': growth_amount,
            'growth_percent': growth_percent,
            'latest_date': sorted_data[-1]['date'],
            'previous_date': sorted_data[-2]['date']
        }

    def company_exists(self, tax_id: str) -> bool:
        """
        Check if a company exists in the dataset.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            True if company exists, False otherwise
        """
        return self.data_loader.company_exists(tax_id)

    def has_financial_data(self, tax_id: str) -> bool:
        """
        Check if a company has any financial data.

        Args:
            tax_id: Company tax ID (EDRPOU)

        Returns:
            True if company has financial data, False otherwise
        """
        dates = self.get_available_dates(tax_id)
        return len(dates) > 0

