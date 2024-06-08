import React from "react";
import {useFormContext} from "react-hook-form";
import {get} from "lodash";

export function TableFormField({name, item, column}: { name: string, item: any, column: any }) {
  function typeMatch(matchType) {
    return column.type === matchType || column.anyOf?.some(({
                                                              format,
                                                              type
                                                            }) => format === matchType || type === matchType)
  }

  if (name === "id") {
    return <input type="hidden" defaultValue={get(item, name)}/>
  } else if (typeMatch("date-time")) {
    return <DateTimeFormField name={name} item={item}/>
  } else if (typeMatch("string")) {
    return <TextFormField name={name} item={item}/>
  } else if (typeMatch("boolean")) {
    return <CheckboxFormField name={name} item={item}/>
  }
}

export function TextFormField({name, item}: { name: string, item: any }) {
  const {register} = useFormContext()
  return (
    <input
      type="text"
      defaultValue={get(item, name)}
      {...register(name)}
      className="input input-primary"
    />
  )
}

export function CheckboxFormField({name, item}: { name: string, item: any }) {
  const {register} = useFormContext()
  return (
    <input
      type="checkbox"
      defaultChecked={get(item, name)}
      {...register(name)}
      className="checkbox checkbox-primary"
    />
  )
}

export function DateTimeFormField({name, item}: { name: string, item: any }) {
  const {register} = useFormContext()
  return (
    <input
      type="datetime-local"
      defaultValue={get(item, name)?.split('.')[0]}
      {...register(name)}
      className="input input-primary"
    />
  )
}