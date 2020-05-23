import dataset  # Import dataset package to provide an abstraction layer with SQL.
from sqlalchemy.exc import NoSuchTableError  # Import of NoSuchTable from sqlalchemy.exc package for SQL error exceptions.

db = dataset.connect('sqlite:///shared_power.db')  # The variable conn creates a connection to an SQLite database named share_power.db.

DB_name = 'shared_power.db'  # DB_name is share_power.db.

def load_create_table(db, table_name):  # Function to create or load a table. Passes parameters conn and table_name.
    """Load a table from a database or create a table in a database if it does not exist.

    The function load_table can only load the table if it exists.

    NoSuchTableError is raised if the table does not exist.

    The function get_table loads or creates a table.

    """

    """Load a table or create it if it doesn't exist yet.

    The function load_table can only load a table if exist, and raises a NoSuchTableError if the table does not already exist in the database.

    The function get_table either loads a table or creates it if it doesn't exist yet. The new table will automatically have an id column unless specified via optional parameter primary_id, which will be used as the primary key of the table.

    Parameters
    ----------
    table_name : str
    conn : dataset.persistence.database.Database
    """
    try:  # The try statement is used to attempt to run the code below, but handles exceptions if unable to run.
        db.load_table(table_name)  # The variable conn initiates a connecti
    except NoSuchTableError as e:
        print('Table {} does not exist. It will be created now'.format(e))
        db.get_table(table_name, primary_id='name', primary_type='String')
        print('Created table {} on database {}'.format(table_name, DB_name))


load_create_table(db, 'test')

