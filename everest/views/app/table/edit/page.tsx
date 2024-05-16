import * as React from "react";
import {useServer} from "./_server/useServer";
import {FloatingRow} from "../../../components/FloatingRow";
import {EditTableView} from "../../../components/EditTableView";
import {TableView} from "./_server";
import {getLocalItem} from "../../../components/utils";
import {FormProvider, useForm, useFormContext} from "react-hook-form";

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

function EditView({view}: {view: TableView}) {
  const {item, table} = useServer()
  const methods = useForm()

  function submit(e) {
    e.preventDefault()
    const data = methods.getValues()
  }

  return (
    <FormProvider {...methods}>
      <form onSubmit={submit}>
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
  )
}

function TableFormField({name, item, column}) {
  function typeMatch(matchType) {
    return column.type === matchType || column.anyOf?.some(({format, type}) => format === matchType || type === matchType)
  }
  if (name === "id") {
    return <input type="hidden" defaultValue={item[name]}/>
  } else if(typeMatch("date-time")) {
    return <DateTimeFormField name={name} item={item}/>
  } else if (typeMatch("string")) {
    return <TextFormField name={name} item={item}/>
  } else if (typeMatch("boolean")) {
    return <CheckboxFormField name={name} item={item}/>
  }
}


function TextFormField({name, item}) {
  const {register} = useFormContext()
  return (
    <input
      type="text"
      defaultValue={item[name]}
      {...register(name)}
    />
  )
}

function CheckboxFormField({name, item}) {
  const {register} = useFormContext()
  return (
    <input
      type="checkbox"
      defaultChecked={item[name]}
      {...register(name)}
    />
  )
}

function DateTimeFormField({name, item}) {
  const {register} = useFormContext()
  return (
    <input
      type="datetime-local"
      defaultValue={item[name]?.split('.')[0]}
      {...register(name)}
    />
  )
}

export default Page;
