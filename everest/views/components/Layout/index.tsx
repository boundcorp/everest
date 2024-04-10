import * as React from 'react';
import {LayoutContext} from "../../app/table/list/_server";
import {TableNavigationSidebar} from "../TableNavigationSidebar";
import {MainPageSidebar, SidebarContext, SidebarProvider} from "./sidebar";
import {FloatingRow} from "../FloatingRow";
import {ArrowLeftEndOnRectangleIcon, ArrowRightStartOnRectangleIcon} from "@heroicons/react/24/outline";

export function Header({title}: { title: string }) {
  const sidebar = React.useContext(SidebarContext)
  return <FloatingRow left={
    <div className={"p-2"}>
      <div className={"float-start px-1 py-2"}>
        <button className={"btn btn-xs bg-base-100"} onClick={sidebar.toggleSidebar}>
          {sidebar.isSidebarOpen ? <ArrowRightStartOnRectangleIcon className={"h-4 w-4"}/> : <ArrowLeftEndOnRectangleIcon className={"h-4 w-4"} />}
        </button>
      </div>
      <a href={"/"}>
        <h1 className={"text-3xl font-bold text-accent"}>{title}</h1>
      </a>
    </div>
  } right={null}/>
}

export default function MainPageLayout({children, layout, title}: {
  children: React.ReactNode,
  layout: LayoutContext,
  title?: string
}) {
  return (
    <PageWrapper>
      <div className={`flex flex-col min-h-full`}>
        <Header title={title || "everest"}/>
        <div className={"flex-1 flex min-vw-100 position-relative"}>
          <MainPageSidebar>
            <TableNavigationSidebar tables={layout.tables}/>
          </MainPageSidebar>
          <div className={"flex-1 p-2 lg:rounded-tl-xl overflow-x-clip z-5"}>
            {children}
          </div>
        </div>
      </div>
    </PageWrapper>
  )
}

export function PageWrapper({children}) {
  return (
    <SidebarProvider>
      {children}
    </SidebarProvider>
  )
}