# sudo pacman -S python-psycopg2 python-sqlalchemy

from sqlalchemy import create_engine, text
import time

# for postgreSQL database credentials can be written as
user = "postgres"
password = "password"
host = "localhost"
port = "5432"
database = "postgres"
# for creating connection string
connection_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"
# SQLAlchemy engine
engine = create_engine(connection_str)
# you can test if the connection is made or not
try:
    with engine.connect() as connection_str:
        print("Successfully connected to the PostgreSQL database")
        engine.connect

except Exception as ex:
    print(f"Sorry failed to connect: {ex}")


# Function to execute and benchmark SQL queries
def benchmark_query(query, repetitions=1, commit=False):
    try:
        with engine.connect() as connection:
            if commit:
                # Enable transaction commit for changes like CREATE TABLE
                with connection.begin():
                    connection.execute(text(query))
            else:
                # For read-only queries or benchmarking
                total_time = 0
                for _ in range(repetitions):
                    start_time = time.perf_counter()
                    connection.execute(text(query))
                    elapsed_time = time.perf_counter() - start_time
                    total_time += elapsed_time
                    print(f"Query executed in: {elapsed_time:.6f} seconds")

                avg_time = total_time / repetitions
                print(
                    f"Average time for {repetitions} repetitions: {avg_time:.6f} seconds"
                )
    except Exception as ex:
        print(f"Failed to execute query: {ex}")


# Test if the connection is made
try:
    with engine.connect() as connection:
        print("Successfully connected to the PostgreSQL database")

    # Example queries
    create_table_query = """
    CREATE TABLE IF NOT EXISTS benchmark_test (
        id SERIAL PRIMARY KEY,
        data TEXT
    )
    """
    insert_query = """
    INSERT INTO benchmark_test (data) VALUES ('Sample data')
    """
    select_query = "SELECT * FROM benchmark_test"

    # Run benchmarks
    print("\nBenchmarking CREATE TABLE:")
    benchmark_query(
        create_table_query, commit=True
    )  # Commit required to persist changes

    print("\nBenchmarking INSERT:")
    benchmark_query(insert_query, repetitions=10)

    print("\nBenchmarking SELECT:")
    benchmark_query(select_query, repetitions=10)

except Exception as ex:
    print(f"Sorry, failed to connect: {ex}")
