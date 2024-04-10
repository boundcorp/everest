from everest.core.builder.sqltable import TableBuilder

if __name__ == '__main__':
    Book = TableBuilder.create('demo.Book', base_classes=['mountaineer.database.sqlmodel.SQLModel'])
    Book.save_to_disk()
