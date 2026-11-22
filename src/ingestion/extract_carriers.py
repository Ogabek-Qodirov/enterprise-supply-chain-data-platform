from src.ingestion.extractor import extract_to_csv


def extract_carriers():
    """Extract carriers from the TMS source system."""

    query = """
        SELECT
            carrier_id,
            carrier_name,
            service_type,
            created_at
        FROM tms.carriers
    """

    extract_to_csv(
        query=query,
        output_filename="tms_carriers.csv"
    )


if __name__ == "__main__":
    extract_carriers()