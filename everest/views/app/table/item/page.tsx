import * as React from "react";
import {useServer} from "./_server/useServer";
import MainPageLayout from "../../../components/Layout";
import {FloatingRow} from "../../../components/FloatingRow";
import {EditTableView} from "../../../components/EditTableView";
import {AdminTable, TableView} from "./_server";
import {getLocalItem} from "../../../components/utils";

const Page = () => {
  const {layout, item, partial_update, linkGenerator} = useServer();
  const table = layout.table
  const view = getLocalItem<TableView>(`${table.table_schema.id}-custom-view`) || table.views[0]

  return (
    <MainPageLayout layout={layout}>
      <FloatingRow left={<h1>{table.table_schema.name}</h1>} right={<EditTableView table={table} view={view}/>}/>
      <DetailView table={table} item={item} view={view} partial_update={partial_update}/>
      <a href={linkGenerator.itemEditController({
        table_id: layout.table_id,
        item_id: layout.item_id,
      })}><button className="btn btn-primary">Edit</button></a>
    </MainPageLayout>
  );
};

function DetailView({table, item, view, partial_update}) {
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
