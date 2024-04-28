# Everest

Playground demonstration of an Admin panel for Mountaineer apps, in the spirit of django admin.

![Preview](/docs/table_view.png)

## Status
Everest is WIP and not ready for production use. I'm working on this during hobby time, so progress may be slow. If you are interested in this project, please let me know by adding a Star!

POC WIP - 
[x] - Automatic list/details/update views for all installed tables
[ ] - Add/Create form for tables
[ ] - Customizable dynamic "Views" for a table, allowing you to hide/format specific columns (similar to Airtable)
[ ] - Authentication

Testing/prototype/playground -
[x] - Interactive Shell (bpython) - `poetry run shell`
[x] - Dynamically create new Tables and save the file to disk - see `core/builder/` 

Planned -
[ ] - View Layouts (e.g. Kanban, Calendar)
[ ] - Actions (e.g. Send Email, Export to CSV)
[ ] - Advanced fields (e.g. File Upload, Rich Text)
[ ] - Permissions
[ ] - Inline relationships (e.g. 1:1, 1:M, M:M)
