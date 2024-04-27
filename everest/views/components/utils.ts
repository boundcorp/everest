import * as React from "react";

export function localStorageState<T>(key: string, defaultValue: T, ssrValue?: T | undefined): [T, (value: T) => void] {
  const [state, setState] = React.useState<T>(getLocalItem<T>(key) ?? ssrValue ?? defaultValue)
  React.useEffect(() => {
    const value = getLocalItem<T>(key)
    if (value) {
      setState(value)
    }
  }, [])
  const set = (value: T) => {
    window?.localStorage.setItem(key, JSON.stringify(value))
    setState(value)
  }
  return [state, set]
}

export function getLocalItem<T>(key: string) {
  if (typeof window !== 'undefined') {
    const value = window.localStorage.getItem(key)
    if (value) {
      return JSON.parse(value) as T
    }
  }
  return null
}