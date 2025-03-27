import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

const sections = {
  "Attitude": ["React", "Next.js", "Tailwind", "CSS", "HTML"],
  "Stress Management": ["Node.js", "Express", "MongoDB", "PostgreSQL", "Django"],
  "Personality": ["JavaScript", "Python", "C++", "Java", "Go"],
  "Group Dynamics": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"]
};

const sectionNames = Object.keys(sections);

const getRandomTile = (section) => {
  const words = sections[section] || [];
  return words[Math.floor(Math.random() * words.length)];
};

export default function RandomTiles() {
  const [tiles, setTiles] = useState([]);
  const [selectedSection, setSelectedSection] = useState(null);
  const [spinning, setSpinning] = useState(false);
  const [sectionSelected, setSectionSelected] = useState(false);
  const [arrowRotation, setArrowRotation] = useState(0);

  const spinWheel = () => {
    setSpinning(true);
    const spins = Math.floor(Math.random() * 4) + 3; // Ensures at least 3 full spins
    const randomIndex = Math.floor(Math.random() * sectionNames.length);
    const newRotation = 360 * spins + randomIndex * (360 / sectionNames.length);
    
    setTimeout(() => {
      setArrowRotation(newRotation % 360);
      setSelectedSection(sectionNames[randomIndex]);
      setTiles([]);
      setSpinning(false);
      setSectionSelected(true);
    }, 3000);
  };

  const drawTile = () => {
    if (selectedSection && tiles.length < 6) {
      setTiles((prevTiles) => [...prevTiles, getRandomTile(selectedSection)]);
    }
    if (tiles.length + 1 >= 6) {
      setSectionSelected(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <div className="relative w-48 h-48 flex items-center justify-center">
        <div className="w-full h-full bg-blue-600 rounded-full flex items-center justify-center text-xl font-bold shadow-lg relative">
          {sectionNames.map((section, index) => (
            <div
              key={index}
              className="absolute w-full text-white font-bold text-center"
              style={{ transform: `rotate(${index * (360 / sectionNames.length)}deg) translateY(-80px)` }}
            >
              {section}
            </div>
          ))}
        </div>
        <motion.div
          className="absolute w-12 h-12 bg-red-500 rounded-full flex items-center justify-center"
          animate={{ rotate: spinning ? arrowRotation : arrowRotation }}
          transition={{ duration: 3, ease: "easeInOut" }}
        >
          <div className="w-0 h-0 border-l-8 border-r-8 border-b-[16px] border-transparent border-b-white"></div>
        </motion.div>
      </div>
      {!sectionSelected && (
        <Button onClick={spinWheel} className="mt-4 bg-green-500 hover:bg-green-600" disabled={spinning}>
          {spinning ? "Spinning..." : "Spin to Select Section"}
        </Button>
      )}
      <div className="flex gap-4 flex-wrap max-w-screen-md justify-center mt-4">
        {tiles.map((tile, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, rotateY: 90 }}
            animate={{ opacity: 1, rotateY: 0 }}
            transition={{ duration: 0.5, delay: index * 0.2 }}
            className="w-24 h-24 flex items-center justify-center text-2xl font-bold bg-gray-800 rounded-lg shadow-lg"
          >
            {tile}
          </motion.div>
        ))}
      </div>
      <Button
        onClick={drawTile}
        className="mt-6 bg-blue-500 hover:bg-blue-600"
        disabled={!selectedSection || tiles.length >= 6}
      >
        {tiles.length >= 6 ? "Limit Reached" : "Draw Tile"}
      </Button>
    </div>
  );
}
