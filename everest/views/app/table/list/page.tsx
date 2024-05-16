import * as React from "react";
import {useServer} from "./_server";
import {TableListItems} from "./ListItems";
import {EditTableView} from "../../../components/EditTableView";
import {FloatingRow} from "../../../components/FloatingRow";


const Page = () => {
  const serverState = useServer();
  const table = serverState.table

  return (
    <>
      <FloatingRow left={<h1>{table.table_schema.name}</h1>} right={<EditTableView table={table} view={table.views[0]}/>}/>
      <TableListItems table={table} view={table.views[0]} items={serverState.items}/>
    </>
  );
};

export default Page;
