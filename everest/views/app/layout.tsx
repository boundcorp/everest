import React, {ReactNode} from "react";
import {useServer} from "./_server";
import {ArrowLeftEndOnRectangleIcon, ArrowRightStartOnRectangleIcon} from "@heroicons/react/24/outline";
import {MainPageSidebar, SidebarContext, SidebarProvider} from "@/components/Layout/sidebar";
import {FloatingRow} from "@/components/FloatingRow";
import {TableNavigationSidebar} from "@/components/TableNavigationSidebar";

export function Header({title}: { title: string }) {
  const layout = useServer();
  const sidebar = React.useContext(SidebarContext)
  return <FloatingRow left={
    <div className={"p-2"}>
      <div className={"float-start px-1 py-2"}>
        <button className={"btn btn-xs bg-base-100"} onClick={sidebar.toggleSidebar}>
          {sidebar.isSidebarOpen ? <ArrowRightStartOnRectangleIcon className={"h-4 w-4"}/> :
            <ArrowLeftEndOnRectangleIcon className={"h-4 w-4"}/>}
        </button>
      </div>
      <a href={"/"}>
        <h1 className={"text-3xl font-bold text-accent"}>{title}</h1>
      </a>
    </div>
  } right={<div className={"p-2"}>
    {layout.user ? <div className={"float-end px-1 py-2"}>
        <a href={"/logout"} className={"btn btn-xs bg-error"}>Logout</a>
      </div> :
      <div className={"float-end px-1 py-2"}>
        <a href={"/login"} className={"btn btn-xs bg-primary"}>Login</a>
      </div>
    }

  </div>}/>
}

export default function Layout({children, title}: {
  children: React.ReactNode,
  title?: string
}) {
  const layout = useServer();
  return (
    <Providers>
      <div className={`flex flex-col min-h-full`}>
        <Header title={title || "everest"}/>
        <div className={"flex-1 flex min-vw-100 position-relative"}>
          <MainPageSidebar>
            <TableNavigationSidebar tables={layout.tables}/>
          </MainPageSidebar>
          <div className={"flex-1 p-2 lg:rounded-tl-xl overflow-x-clip z-5 bg-base-200"}>
            {children}
          </div>
        </div>
      </div>
    </Providers>
  )
}

export function Providers({children}: { children: ReactNode }) {
  return (
    <SidebarProvider>
      {children}
    </SidebarProvider>
  )
}