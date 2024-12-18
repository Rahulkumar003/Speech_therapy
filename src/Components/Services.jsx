import React from "react";

import { RiMicroscopeLine } from "react-icons/ri";

import { MdHealthAndSafety } from "react-icons/md";
import { FaHeartbeat } from "react-icons/fa";
import Button from "../Layouts/Button";
import ServicesCard from "../Layouts/ServicesCard";
import SpeechAnalysis from "./SpeechAnalysis";
import AITherapist from "./Ai_therapist";
const Services = () => {
  const icon1 = (
    <RiMicroscopeLine size={35} className=" text-backgroundColor" />
  );
  const icon2 = (
    <MdHealthAndSafety size={35} className=" text-backgroundColor" />
  );
  const icon3 = <FaHeartbeat size={35} className=" text-backgroundColor" />;

  return (
    <div className=" min-h-screen flex flex-col justify-center lg:px-32 px-5 pt-24 lg:pt-16">
      <div className=" flex flex-col items-center justify-between">
        <div>
          <h1 className=" text-4xl font-semibold text-center lg:text-center">
            Our Services
          </h1>
          <p className=" mt-2 text-center lg:text-center">
            Explore innovative solutions designed to enhance communication and well-being.
          </p>
        </div>
      </div>
      <div className=" flex flex-col lg:flex-row gap-5 pt-14">
        <ServicesCard 
          icon={icon1} 
          title="Speech Analysis" 
          description="Advanced tools for analyzing speech patterns, tone, and clarity, tailored for diagnostics and improvement." 
          link="/speech_analysis"
        />
        <ServicesCard 
          icon={icon2} 
          title="AI Therapists" 
          description="AI-powered virtual therapists offering expert insights and solutions for speech-related challenges, enhancing communication and understanding." 
          link="/ai_therapist"
        />
        <ServicesCard 
          icon={icon3} 
          title="The Speech Resource Library" 
          description="A comprehensive repository offering tools, datasets, and resources for speech and language research." 
          link="/repository"
        />
      </div>
    </div>
  );
};

export default Services;