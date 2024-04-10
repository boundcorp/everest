import * as React from "react";

export function FloatingRow({left, right}: { left: React.ReactNode, right: React.ReactNode }) {
  return (
    <div className={`w-full flex mb-1`}>
      <div className="flex-1">
        {left}
      </div>
      <div className="flex-0">
        {right}
      </div>
    </div>
  )
}