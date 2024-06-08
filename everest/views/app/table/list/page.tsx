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
      <FloatingRow left={<h1 className={"text-3xl font-bold text-accent pb-2"}>{table.name} List</h1>}
                   right={<EditTableView table={table} view={table.views[0]}/>}/>
      <TableListItems table={table} view={table.views[0]} items={serverState.items}/>
    </>
  );
};

export default Page;
