import * as React from "react";
import {useServer} from "./_server/useServer";
import {FloatingRow} from "../../../components/FloatingRow";
import {EditTableView} from "../../../components/EditTableView";
import {getLocalItem} from "../../../components/utils";
import {TableView} from "@/app/_server";

const Page = () => {
  const {table, item, linkGenerator} = useServer();
  const view = getLocalItem<TableView>(`${table.table_schema.id}-custom-view`) || table.views[0]

  return (
    <>
      <FloatingRow left={<h1>{table.table_schema.name}</h1>} right={<EditTableView table={table} view={view}/>}/>
      <DetailView table={table} item={item} view={view} />
      <a href={linkGenerator.itemEditController({
        table_id: table.table_schema.id,
        item_id: item?.id as string || "0",
      })}><button className="btn btn-primary">Edit</button></a>
    </>
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
              <div>{item?.[column]}</div>
            </div>
          )
        )
      }
    </div>
  )
}

export default Page;
