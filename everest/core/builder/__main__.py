from everest.core.builder.sqltable import SQLModelTableBuilder

if __name__ == '__main__':
    TableView = SQLModelTableBuilder.create_single('admin.TableView', base_classes=['mountaineer.database.sqlmodel.SQLModel'])
    TableView.add_field('table', 'str')
    TableView.add_field('stub', 'str')
    TableView.add_field('description', 'str')

    TableViewColumn = SQLModelTableBuilder.create_single('admin.TableViewColumn', base_classes=['mountaineer.database.sqlmodel.SQLModel'])
    TableViewColumn.add_field('column', 'str')
    TableViewColumn.add_foreign_key('table', TableView, 'columns')

    TableView.save_to_disk()
    TableViewColumn.save_to_disk()
