import * as React from "react";

export const TableListItems = ({view, table, items}) => {
  return (
    <table className={"w-full table rounded-0 table-zebra table-pin-rows table-pin-cols bg-base-300"}>
      <thead>
      <tr>
        <th>ID</th>
        {view.columns.map((column) => (
          <th key={column}>{table.table_schema.properties[column].title}</th>
        ))}
      </tr>
      </thead>
      <tbody>
      {items.map((item) => (
        <tr key={item.id}>
          <th className={"max-w-60"}>
            <a href={`/table/${table.table_schema.id}/${item.id}`}>
              <button className={"btn btn-sm btn-accent"}>{item.id}</button>
            </a>
          </th>
          {view.columns.map((column) => (
            <td key={column}>{item[column]}</td>
          ))}
        </tr>
      ))}
      </tbody>
    </table>
  );
}