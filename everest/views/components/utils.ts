import * as React from "react";
import {FieldValues, UseFormReturn} from "react-hook-form";
import {FormErrorException} from "@/auth/login/_server";

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

export function cookieState<T>(key: string, defaultValue: T, ssrValue?: T | undefined): [T, (value: T) => void] {
  const [state, setState] = React.useState<T>(getCookieItem<T>(key) ?? ssrValue ?? defaultValue);

  React.useEffect(() => {
    const value = getCookieItem<T>(key);
  }, []);

  const set = (value: T) => {
    setCookie(key, JSON.stringify(value), 365); // Set cookie with 1-year expiry
    setState(value);
  };

  return [state, set];
}

export function getCookieItem<T>(key: string) {
  const name = key + "=";
  const decodedCookie = typeof(document) !== 'undefined' ? decodeURIComponent(document.cookie) : "";
  const ca = decodedCookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return JSON.parse(c.substring(name.length, c.length)) as T;
    }
  }
  return null;
}

function setCookie(name: string, value: string, days: number) {
  const d = new Date();
  d.setTime(d.getTime() + (days*24*60*60*1000));
  const expires = "expires="+ d.toUTCString();
  if(typeof document !== 'undefined')
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

export type FormSubmitOptions<R> = {
  onSuccess?: (response: R) => void,
  onFormError?: (e: FormErrorException) => void
  onError?: (e: unknown) => void
}

export function handleFormSubmit<T extends FieldValues, R>(form: UseFormReturn<T>, action: (data: T) => Promise<R>, options?: FormSubmitOptions<R>) {
  return form.handleSubmit(async (values) => {
    try {
      const response = await action(values);
      if (options?.onSuccess) {
        options.onSuccess(response);
      }
    } catch (e) {
      if (e instanceof FormErrorException) {
        console.error("Form Error", e.body.detail);
        form.setError("root.error", {message: e.body.detail})
        if (options?.onFormError) {
          options.onFormError(e);
        }
      } else {
        console.error("Error", e);
        if (options?.onError) {
          options.onError(e);
        }
      }
    }
  })
}