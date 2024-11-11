from models.__init__ import ToDo, Task, NewTask, ResponseMessageBD
from sqlmodel import create_engine, SQLModel, Session, select, col

conn_string = 'postgresql+psycopg://postgres:!localhost:5433/homedb'

engine = create_engine(conn_string)

def create_tables():
    SQLModel.metadata.create_all(engine)

def add_row(row: ToDo) -> ToDo:
    with Session(engine) as session:
        session.add(row)
        session.commit()
        session.refresh(row)
    return row

def select_row_by_id(row_id: int) -> ToDo:
    with Session(engine) as session:
        statement = select(ToDo).where(col(ToDo.id) == row_id)
        result = session.exec(statement).first()
        return result

def update_row_by_id(row_id: int, data: NewTask) -> ToDo | ResponseMessageBD:
    new_row = select_row_by_id(row_id)
    if new_row:
        data_atters = data.model_dump().keys()
        for attr in data_atters:
            setattr(new_row, attr, getattr(data, attr))
        with Session(engine) as session:
            session.add(new_row)
            session.commit()
            session.refresh(new_row)
        return new_row
    return ResponseMessageBD(**{'message': 'now row found', 'row': None})

def delete_row_by_id(row_id: int) -> ResponseMessageBD:
    delete_row = select_row_by_id(row_id)
    if delete_row:
        with Session(engine) as session:
            session.delete(delete_row)
            session.commit()
        return ResponseMessageBD(**{'message': 'row deleted', 'row': Task(**delete_row.model_dump())})
    return ResponseMessageBD(**{'message': 'no row found', 'row': None})