import * as React from "react";
import {BeakerIcon} from "@heroicons/react/24/outline";

export function EditTableView({table, view}) {
  const ref = React.useRef(null);

  function toggleHandler(column) {
    return function (e) {
      const newView = {...view}
      if (e.target.checked) {
        newView.columns.push(column)
      } else {
        newView.columns = newView.columns.filter((c) => c !== column)
      }
      window.localStorage.setItem(`${table.table_schema.id}-custom-view`, JSON.stringify(newView))
    }
  }

  return (<>
    <button className="btn btn-accent btn-sm" onClick={() => ref.current.showModal()}>
      <BeakerIcon className={"h-6 w-6"}/>
    </button>
    <dialog id="configure_view" className="modal modal-bottom sm:modal-middle" ref={ref}>
      <div className="modal-box">
        <h3 className="font-bold text-lg">{table.table_schema.name}</h3>
        <table className="py-4">
          {Object.keys(table.table_schema.properties).map((column) => (
            <tr key={column}>
              <td className={"pb-1"}>{table.table_schema.properties[column].title}</td>
              <td>
                <input type="checkbox" className={"toggle"} defaultChecked={view.columns.includes(column)} onClick={toggleHandler(column)}/>
              </td>
            </tr>
          ))}

        </table>
        <div className="modal-action">
          <form method="dialog">
            {/* if there is a button in form, it will close the modal */}
            <button className="btn">Close</button>
          </form>
        </div>
      </div>
    </dialog>
  </>)
}