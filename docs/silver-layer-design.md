
# Silver Layer Design

## 1. Purpose

The Silver layer transforms raw Bronze datasets into
cleaned, standardized, and analytically reliable datasets.

Bronze data must remain unchanged.

## 2. Input and Output

Input:
- data/bronze/

Output:
- data/silver/

Storage format:
- Parquet

## 3. Transformation Rules

1. Preserve source identifiers.
2. Convert numeric columns into appropriate numeric types.
3. Convert date and timestamp columns into proper datetime types.
4. Preserve legitimate NULL values.
5. Validate primary keys and foreign-key relationships.
6. Detect duplicates without silently deleting records.
7. Preserve source data in Bronze.
8. Make transformations repeatable.

## 4. Data Quality

Before transformation:
- Run Bronze verification.
- Validate primary keys.
- Validate foreign-key relationships.

After transformation:
- Verify output record counts.
- Verify data types.
- Verify primary-key uniqueness.
- Verify foreign-key relationships.

## 5. Output Structure

data/
    bronze/
    silver/
        oms/
        wms/
        tms/
        finance/

## 6. Processing Architecture

Bronze CSV
    |
    v
Data Quality Validation
    |
    v
Type Conversion
    |
    v
Data Standardization
    |
    v
Silver Parquet

## 7. Important Principles

- Never modify Bronze files during transformation.
- Never silently discard invalid records.
- Keep transformations reproducible.
- Log transformation results.
- Maintain data lineage between Bronze and Silver.
