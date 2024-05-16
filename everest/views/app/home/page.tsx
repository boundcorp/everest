import * as React from "react";
import {useServer} from "./_server";

const Home = () => {
  const serverState = useServer();

  return (
    <>
      here
    </>
  );
};

export default Home;
