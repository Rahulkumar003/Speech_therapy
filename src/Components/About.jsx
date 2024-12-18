import React from "react";
import img from "../assets/about.jpg";

const About = () => {
  return (
    <div className=" min-h-screen flex flex-col lg:flex-row justify-between items-center lg:px-32 px-5 pt-24 lg:pt-16 gap-5">
      <div className=" w-full lg:w-3/4 space-y-4">
        <h1 className=" text-4xl font-semibold text-center lg:text-start">About Us</h1>
        <p className=" text-justify lg:text-start">
          Welcome to SpeakSmart, your ultimate destination for innovative speech therapy solutions. Our platform is designed to empower individuals by analyzing their voice and providing personalized therapy options. Whether you prefer guidance from professional therapists or AI-driven therapy sessions, we cater to your unique needs.
        </p>
        <p className="text-justify lg:text-start">
          At SpeakSmart, we believe in the power of technology to transform speech therapy. Our advanced analysis tools offer insights into your vocal patterns, helping you understand and improve your speech. With our AI therapy, you can practice and enhance your skills at your own pace, anytime and anywhere.
        </p>
        <p className="text-justify lg:text-start">
          Dive into our extensive repository, brimming with resources to boost your speech in a fun and engaging way. Experience a gamified learning journey that makes speech improvement enjoyable and rewarding. Join us at SpeakSmart and take the first step towards a more confident and articulate you!
        </p>
      </div>
      <div className=" w-3/4 lg space-y-4">
        <img className=" rounded-lg" src={img} alt="img" />
      </div>
    </div>
  );
};

export default About;