import logging
import sys
from pathlib import Path

from flask import Flask, render_template, request, jsonify

from services.data_loader import DataLoader
from services.financial_service import FinancialService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global service instances
data_loader = None
financial_service = None

def initialize_services():
    global data_loader, financial_service

    try:
        # Determine data directory
        base_dir = Path(__file__).parent
        data_dir = base_dir / 'data'

        firms_path = data_dir / 'firms.csv'
        fin_values_path = data_dir / 'fin_values.csv'

        data_loader = DataLoader()
        # Load CSV data
        data_loader.load_data(str(firms_path), str(fin_values_path))

        # Initialize financial service
        financial_service = FinancialService(data_loader)

        # Get statistics
        stats = data_loader.get_stats()
        logger.info(f"Data loaded successfully:")
        logger.info(f"  - Companies: {stats['companies_count']}")
        logger.info(f"  - Financial records: {stats['financial_records_count']}")
        logger.info(f"  - Companies with data: {stats['unique_companies_with_data']}")

    except Exception as e:
        sys.exit(1)

initialize_services()

@app.route("/")
def index():
    tax_id = "00446368"

    # Get company information
    company_obj = financial_service.get_company_by_tax_id(tax_id)

    return render_template('index.html',
                            company = company_obj)

@app.route('/api/revenue/<tax_id>')
def api_revenue(tax_id):
    # Get revenue data
    revenue_data = financial_service.get_revenue_data(tax_id)
    logger.info(f"Revenue data for {tax_id}: {revenue_data}")

    return jsonify(revenue_data)

@app.route('/api/balance/<tax_id>')
def api_balance(tax_id):
    # Get date parameter
    date = request.args.get('date')
    # Get balance data
    balance_data = financial_service.get_balance_data(tax_id, date)
    logger.info(f"Balance data for {tax_id} on {date}: {balance_data}")

    return jsonify(balance_data)

if __name__ == "__main__":
    app.run(debug=True)