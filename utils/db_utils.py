from sqlmodel import create_engine

sqlite_dir = "Data/"
sqlite_filename = "Eat_Right.sqlite"

data_base_path = f"{sqlite_dir}{sqlite_filename}"

engine = create_engine(f"sqlite:///{data_base_path}")
