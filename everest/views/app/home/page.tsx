import * as React from "react";
import {useServer} from "@/app/_server"

const Home = () => {
  const serverState = useServer();

  return (
    <>
      <pre>
        {JSON.stringify(serverState, null, 2)}
      </pre>
    </>
  );
};

export default Home;
