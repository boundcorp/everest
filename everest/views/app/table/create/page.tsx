import * as React from "react";
import {useServer} from "./_server/useServer";
import {FloatingRow} from "@/components/FloatingRow";
import {EditTableView} from "@/components/EditTableView";
import {TableView} from "./_server";
import {getLocalItem} from "@/components/utils";
import {FormProvider, useForm} from "react-hook-form";
import {TableFormField} from "@/components/FormFields/common";

const Page = () => {
  const {table} = useServer();
  const view = getLocalItem<TableView>(`${table.table_schema.id}-custom-view`) || table.views?.[0] || {columns: []}

  return (
    <>
      <FloatingRow left={<h1 className={"text-3xl font-bold text-accent pb-2"}>Create {table.name}</h1>}
                   right={<EditTableView table={table} view={view}/>}/>
      <CreateView view={view}/>
    </>
  );
};

function CreateView({view}: { view: TableView }) {
  const {table, create} = useServer()
  const methods = useForm()
  const defaultValues = {}

  async function submit(e) {
    e.preventDefault()
    const data = methods.getValues()
    await create({requestBody: {data}, table_id: table.table_schema.id});

  }

  return (
    <div className={"flex justify-center items-center h-full"}>
      <div className={"w-96 p-4 bg-base-100 rounded-xl"}>
        <FormProvider {...methods}>
          <form onSubmit={submit}>
            {
              view.columns.map(
                (column) => (
                  <div key={column} className="mb-1">
                    <h2>{column}</h2>
                    <TableFormField name={column} item={defaultValues} column={table.table_schema.properties[column]}/>
                  </div>
                )
              )
            }
            <button className="btn btn-primary" type={"submit"}>Save</button>
          </form>
        </FormProvider>
      </div>
    </div>
  )
}


export default Page