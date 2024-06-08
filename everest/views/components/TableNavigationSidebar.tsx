import * as React from "react";
import {groupBy} from 'lodash';

export const TableNavigationSidebar = ({tables}) => {
  const groups = groupBy(Object.keys(tables), (id: string) => tables[id].table_schema.app_label);
  return (
    <div className="p-1">
      <ul>
        {
          Object.keys(groups).map(
            (group) => (
              <li key={group}>
                <h2 className={"text-lg font-bold text-accent"}>{group}</h2>
                {groups[group].map((id) => (
                  // @ts-ignore
                  <li key={id}>
                    <a href={`/table/${id}`}>
                      <button className={"btn btn-sm w-full mb-1 btn-secondary rounded-sm"}>
                        {tables[id].table_schema.name}
                      </button>
                    </a>
                  </li>
                ))}
              </li>)
          )
        }
      </ul>
    </div>
  );
}