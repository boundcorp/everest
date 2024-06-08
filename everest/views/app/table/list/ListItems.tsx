import * as React from "react";
import {AdminTable, TableView} from "@/app/table/list/_server";
import {HTMLProps} from "react";

type Navigation = {
  hoverRow?: number;
  chosenRow?: number;
  chosenColumn?: string;
  editingRow?: number;
  editingColumn?: string;
}

export const TableListItems = ({view, table, items}: {
  view: TableView,
  table: AdminTable,
  items: Array<Record<string, boolean | null | number | string> & { id: string | number }>
}) => {
  const [nav, setNav] = React.useState<Navigation>({})

  function HoverCell({rowIdx, colIdx, column, item}: { rowIdx: number, colIdx: number, column: string, item: any }) {
    const hoverRow = (nav.hoverRow === rowIdx)
    const isChosen = (nav.chosenRow === rowIdx && nav.chosenColumn === column)

    return (
      <td
        onMouseEnter={() => setNav({...nav, hoverRow: rowIdx})}
        onMouseLeave={() => setNav({...nav, hoverRow: undefined})}
        onClick={() => setNav({chosenRow: rowIdx, chosenColumn: column})}
        onDoubleClick={() => setNav({chosenRow: rowIdx, chosenColumn: column, editingRow: rowIdx, editingColumn: column})}
        className={isChosen ? `border-2 border-primary bg-opacity-10 bg-gray-500` : hoverRow ? `bg-opacity-10 bg-gray-500` : undefined}>
        {item[column]}
      </td>
    )
  }

  return (
    <table className={"w-full table rounded-0 table-zebra table-pin-rows table-pin-cols bg-base-300"}>
      <thead>
      <tr>
        <th colSpan={view.columns.length + 1} className={"text-center"}>
        </th>
      </tr>
      <tr>
        {view.columns.map((column) => (
          <th key={column}>{table.table_schema.properties[column].title}</th>
        ))}
      </tr>
      </thead>
      <tbody>
      {items.map((item, rowIdx) => (
        <tr key={item.id}>
          {view.columns.map((column, colIdx) => (
            <HoverCell key={column} rowIdx={rowIdx} colIdx={colIdx} column={column} item={item}/>
          ))}
        </tr>
      ))}
      </tbody>
    </table>
  );
}