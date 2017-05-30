from Database_init import Base, User, db


def create_table():
  """Creates the db tables."""
  Base.metadata.create_all(db)


if __name__ == '__main__':
    create_table()
