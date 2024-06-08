# Everest

Playground demonstration of an Admin panel for Mountaineer apps, in the spirit of django admin.

![Preview](/docs/table_view.png)

## Status & Roadmap
Everest is WIP and not ready for production use. I'm working on this during hobby time, so progress may be slow. If you are interested in this project, please let me know by adding a Star!

### POC (WIP) - 
- [x] Automatic list/details/update views for all installed tables
- [X] Authentication
- [X] Session and Visitor logging, hourly cleanup job
- [x] Create/Edit forms for tables
- [ ] Background Tasks and Task Executor
- [ ] Customizable dynamic "Views" for a table, allowing you to hide/format specific columns (similar to Airtable)
- [ ] Object Storage Handler, File Fields, Image Fields
- [ ] Automatic Backups to Object Storage
- [ ] CI and Devops
  - [ ] Dockerize backend, devcontainer
  - [ ] Add minio for file storage
  - [ ] Helm Chart / K8s manifests
  - [ ] CI/CD pipeline (github)

### Testing/prototype/playground -
- [x] Interactive Shell (bpython) - `poetry run shell`
- [x] Dynamically create new Tables and save the file to disk - see `core/builder/` 

### Planned -
- [ ] View Layouts (e.g. Kanban, Calendar)
- [ ] Actions (e.g. Send Email, Export to CSV)
- [ ] Advanced fields (e.g. postgis, Rich Text)
- [ ] Permissions
- [ ] Inline relationships (e.g. 1:1, 1:M, M:M)
