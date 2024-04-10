import * as React from "react";
import {useServer} from "./_server/useServer";
import MainPageLayout from "../../../components/Layout";
import {FloatingRow} from "../../../components/FloatingRow";
import {EditTableView} from "../../../components/EditTableView";
import {TableView} from "./_server";
import {getLocalItem} from "../../../components/utils";

const Page = () => {
  const serverState = useServer();
  const table = serverState.layout.tables[serverState.id]
  const view = getLocalItem<TableView>(`${table.table_schema.id}-custom-view`) || table.views[0]

  return (
    <MainPageLayout layout={serverState.layout}>
      <FloatingRow left={<h1>{table.table_schema.name}</h1>} right={<EditTableView table={table} view={view}/>}/>
      <DetailView table={table} item={serverState.item} view={view}/>
    </MainPageLayout>
  );
};

function DetailView({table, item, view}) {
  return (
    <div>
      {
        view.columns.map(
          (column) => (
            <div key={column} className="mb-1">
              <h2>{column}</h2>
              <div>{item[column]}</div>
            </div>
          )
        )
      }
    </div>
  )
}

export default Page;
