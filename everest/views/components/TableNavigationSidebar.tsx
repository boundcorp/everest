import * as React from "react";

export const TableNavigationSidebar = ({tables}) => (
  <div className="p-1">
    <ul>
      {
        Object.keys(tables).map(
          (id) => (
            <li key={id}>
              <a href={`/table/${id}`}>
                <button className={"btn btn-sm w-full mb-1 btn-secondary"}>
                  {tables[id].table_schema.name}
                </button>
              </a>
            </li>
          )
        )
      }
    </ul>
  </div>
);