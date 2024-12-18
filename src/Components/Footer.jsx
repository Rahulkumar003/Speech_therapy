import React from "react";
import { Link } from "react-scroll";

const Footer = () => {
  return (
    <div className=" bg-backgroundColor text-white rounded-t-3xl mt-8 md:mt-0">
      <div className="flex flex-col md:flex-row justify-between p-8 md:px-32 px-5">
        <div className=" w-full md:w-1/2">
          <h1 className=" font-semibold text-xl pb-4">SpeakSmart</h1>
          <p className=" text-sm">
          Our innovation and ideas are a reflection of Angshu Sir's guidance and inspiration. This project is a result of his support and our team’s dedication. Thank you for making it possible!
          </p>
        </div>
        <div>
          <Link
            to="about"
            spy={true}
            smooth={true}
            duration={500}
            className=" font-medium text-xl pb-4 pt-5 md:pt-0 hover:text-hoverColor transition-all cursor-pointer"
          >
            About Us
          </Link>
        </div>
        <div>
          <Link
            to="services"
            spy={true}
            smooth={true}
            duration={500}
            className=" font-medium text-xl pb-4 pt-5 md:pt-0 hover:text-hoverColor transition-all cursor-pointer"
          >
            Services
          </Link>
        </div>
        <div>
          <Link
            to="doctors"
            spy={true}
            smooth={true}
            duration={500}
            className=" font-medium text-xl pb-4 pt-5 md:pt-0 hover:text-hoverColor transition-all cursor-pointer"
          >
            Therapy
          </Link>
        </div>
        <div>
          <Link
            to="repository"
            spy={true}
            smooth={true}
            duration={500}
            className=" font-medium text-xl pb-4 pt-5 md:pt-0 hover:text-hoverColor transition-all cursor-pointer"
          >
            Repository
          </Link>
        </div>
      </div>
      <div>
        <p className=" text-center  -mt-5 ">
        Designed and Developed by
          <span className=" text-hoverColor"> Rahul kumar</span>
        </p>
      </div>
    </div>
  );
};

export default Footer;