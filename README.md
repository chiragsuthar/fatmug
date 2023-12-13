# Vendor Management System

This is a Django-based Vendor Management System. It provides a set of RESTful APIs to manage vendors and purchase orders, and calculate vendor performance metrics.

## Features

- Vendor management: Create, retrieve, update, and delete vendors.
- Purchase order management: Create, retrieve, update, and delete purchase orders.
- Vendor performance metrics: Calculate on-time delivery rate, quality rating average, average response time, and fulfillment rate for each vendor.

## Models

- `Vendor`: Stores essential information about each vendor and their performance metrics.
- `PurchaseOrder`: Captures the details of each purchase order and is used to calculate various performance metrics.

## API Endpoints

- `GET /api/vendors/`: List all vendors.
- `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details.
- `GET /api/vendors/{vendor_id}/performance`: Retrieve a vendor's performance metrics.
- `GET /api/purchase_orders/`: List all purchase orders.
- `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
- `POST /api/purchase_orders/{po_id}/acknowledge`: Acknowledge a purchase order.

## Setup

1. Clone the repository: `git clone https://github.com/chiragsuthar/vendor_management_system.git`
2. Navigate to the project directory: `cd vendor_management_system`
3. Install the requirements: `pip install -r requirements.txt`
4. Run the migrations: `python manage.py makemigrations && python manage.py migrate`
5. Start the server: `python manage.py runserver`

## Usage

You can access the API endpoints from your web browser or a tool like Postman or curl.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
