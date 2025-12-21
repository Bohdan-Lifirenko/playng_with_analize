"""
Data models for Ukrainian Company Financial Data Viewer.

This module contains dataclass models for representing company and financial data
loaded from CSV files.
"""

from .company import Company
from .financial import FinancialRecord

__all__ = ['Company', 'FinancialRecord']

