from src.ingestion.extractor import extract_to_csv


def extract_employees():
    """Extract employees from the WMS source system."""

    query = """
        SELECT
            employee_id,
            warehouse_id,
            full_name,
            job_title,
            hire_date
        FROM wms.employees
    """

    extract_to_csv(
        query=query,
        output_filename="wms_employees.csv"
    )


if __name__ == "__main__":
    extract_employees()