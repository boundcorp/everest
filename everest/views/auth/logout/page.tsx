import React, {useEffect} from 'react';
import {useServer} from './_server';

export default function LoginPage() {
  const server = useServer();
  useEffect(() => {
    server.logout().then(() => {
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
    });
  }, [])
  return (
    <div className={"flex justify-center items-center h-full"}>
      <div className={"w-96 p-4 bg-base-100 rounded-xl"}>
        <h1 className={"text-3xl font-bold text-accent pb-2"}>Logged Out</h1>
        <p>You have been logged out.</p>
      </div>
    </div>
  );
}