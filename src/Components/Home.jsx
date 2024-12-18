import React from "react";
import Button from "../Layouts/Button";


const Home = () => {
  return (
    <div className=" min-h-screen flex flex-col justify-center lg:  px-32 px-5 text-white bg-[url('assets/img/home.jpg')] bg-no-repeat bg-cover bg-center opacity-95" style={{ backgroundPosition: 'center 0%' }}>
      <div className=" w-full lg space-y-5 mt-12">
        <h1 className=" text-5xl font-bold leading-tight text-36ae9a">
        Unlock Your Voice, Unlock Your Potential

        </h1>
        <p className=" text-center text-2xl font-bold leading-tight text-36ae9a">
        Empowering you to communicate with confidence, one word at a time.

        </p>
      </div>
    </div>
  );
};

export default Home;