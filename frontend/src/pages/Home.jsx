import React from "react";
import { DataTable } from "../components/DataTable";
import { json, useLoaderData } from "react-router-dom";

const Home = () => {
  const data = useLoaderData();
  console.log(data)
  return (
    <div>
      <DataTable data={data} />
    </div>
  );
};

export default Home;

export const loader = async () => {
  const response = await fetch("http://localhost:5002/messages_and_orders");

  if (!response.ok) {
    throw json(
      { message: "Could not fetch messages and orders." },
      {
        status: 500,
      }
    );
  } else {
    const resData = await response.json();
    return resData;
  }
};
