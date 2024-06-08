import * as React from "react";
import {useServer} from "./_server/useServer";
import {FloatingRow} from "../../../components/FloatingRow";
import {EditTableView} from "../../../components/EditTableView";
import {AdminTableRow, TableView} from "./_server";
import {getLocalItem, handleFormSubmit} from "../../../components/utils";
import {FormProvider, useForm} from "react-hook-form";
import {TableFormField} from "@/components/FormFields/common";

const Page = () => {
  const {table} = useServer();
  const view = getLocalItem<TableView>(`${table.table_schema.id}-custom-view`) || table.views[0]

  return (
    <>
      <FloatingRow left={<h1>{table.table_schema.name}</h1>} right={<EditTableView table={table} view={view}/>}/>
      <EditView view={view}/>
    </>
  );
};

function EditView({view}: { view: TableView }) {
  const {item, table, partial_update, linkGenerator} = useServer()
  type GenericForm = Record<string, boolean | null | number | string>
  const form = useForm<GenericForm>()

  const submit = async (data: GenericForm) => {
    console.log("Sending data", data)
    return await partial_update({table_id: table.table_schema.id, requestBody: {data: {...data, id: item.id}}})
  }

  return (
    <div className={"flex justify-center items-center h-full"}>
      <div className={"w-96 p-4 bg-base-100 rounded-xl"}>
        <FormProvider {...form}>
          <form
            onSubmit={handleFormSubmit(form, submit, {onSuccess: (r) => window.location.pathname = linkGenerator.tableItemController({table_id: table.table_schema.id, item_id: r.sideeffect.item.id})})}>
            {
              view.columns.map(
                (column) => (
                  <div key={column} className="mb-1">
                    <h2>{column}</h2>
                    <TableFormField name={column} item={item} column={table.table_schema.properties[column]}/>
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


export default Page;
