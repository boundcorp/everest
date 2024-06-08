import React from "react";
import {FloatingRow} from "@/components/FloatingRow";

export function Header({title}: { title: string }) {
  return <FloatingRow left={
    <div className={"p-2"}>
      <a href={"/"}>
        <h1 className={"text-3xl font-bold text-accent"}>{title}</h1>
      </a>
    </div>
  } right={null}/>
}

export default function Layout({children, title}: {
  children: React.ReactNode,
  title?: string
}) {
  return (
    <div className={`flex flex-col min-h-full`}>
      <Header title={title || "everest"}/>
      <div className={"flex-1 flex min-vw-100 position-relative"}>
        <div className={"flex-1 p-2 lg:rounded-tl-xl overflow-x-clip z-5 bg-base-200"}>
          {children}
        </div>
      </div>
    </div>
  )
}