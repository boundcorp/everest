import * as React from "react";
import {cookieState} from "../utils";
import {BackwardIcon, ForwardIcon} from "@heroicons/react/24/outline";
import { useServer } from "@/app/_server";

export const SidebarContext = React.createContext({
  isSidebarOpen: true,
  toggleSidebar: () => {
  }
})

export const SidebarProvider = ({children}: { children: React.ReactNode }) => {
  const ssrOpen = useServer()?.sidebar_open
  const [isSidebarOpen, setIsSidebarOpen] = cookieState('sidebarOpen', true, ssrOpen)
  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen)

  return (
    <SidebarContext.Provider value={{isSidebarOpen, toggleSidebar}}>
      {children}
    </SidebarContext.Provider>
  )
}

export function MainPageSidebar({children}: { children: React.ReactNode }) {
  return (
    <>
      <LargeScreenSidebarDocked>
        {children}
      </LargeScreenSidebarDocked>
      <SmallScreenFloatingMenu>
        {children}
      </SmallScreenFloatingMenu>
    </>
  )
}

export function SmallScreenFloatingMenu({children}: { children: React.ReactNode }) {
  const {isSidebarOpen} = React.useContext(SidebarContext)
  return <div className={`lg:invisible position-relative w-0 z-10`}>
    <div className={`position-fixed bottom-0 right-0 w-auto bg-base-200 rounded-r-xl p-2
    ${isSidebarOpen ? 'min-w-40 w-1/4 max-w-80' : 'w-0 invisible'}`}>
      {children}
    </div>
  </div>
}

export function LargeScreenSidebarDocked({children}: { children: React.ReactNode }) {
  const {isSidebarOpen, toggleSidebar} = React.useContext(SidebarContext)
  const icon = "h-3 w-3"
  return <div className={"flex w-0 lg:w-auto invisible lg:visible"}>
    <div className={`flex-1
        ${isSidebarOpen ? 'min-w-40 w-1/4 max-w-80' : 'w-0 invisible'}`}>
      {children}
    </div>
    <div onClick={toggleSidebar}
         className={"flex-0 my-2 text-center flex items-center cursor-pointer hover:bg-base-300 rounded-xl"}>
      {isSidebarOpen ? <BackwardIcon className={icon}/> : <ForwardIcon className={icon}/>}
    </div>
  </div>
}