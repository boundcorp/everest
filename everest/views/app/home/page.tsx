import * as React from "react";
import {useServer} from "./_server";
import MainPageLayout from "../../components/Layout";

const Home = () => {
  const serverState = useServer();

  return (
    <MainPageLayout layout={serverState.layout} title={"Home"}>
      here
    </MainPageLayout>
  );
};

export default Home;
