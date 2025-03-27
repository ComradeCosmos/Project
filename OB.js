import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

const sections = {
  "Frontend": ["React", "Next.js", "Tailwind", "CSS", "HTML"],
  "Backend": ["Node.js", "Express", "MongoDB", "PostgreSQL", "Django"],
  "Programming": ["JavaScript", "Python", "C++", "Java", "Go"],
  "DevOps": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"]
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

  const spinWheel = () => {
    setSpinning(true);
    setTimeout(() => {
      const randomSection = sectionNames[Math.floor(Math.random() * sectionNames.length)];
      setSelectedSection(randomSection);
      setTiles([]);
      setSpinning(false);
    }, 2000);
  };

  const drawTile = () => {
    if (selectedSection && tiles.length < 6) {
      setTiles((prevTiles) => [...prevTiles, getRandomTile(selectedSection)]);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <motion.div
        className="w-32 h-32 flex items-center justify-center text-xl font-bold bg-blue-600 rounded-full shadow-lg mb-4"
        animate={{ rotate: spinning ? 360 : 0 }}
        transition={{ duration: 2, ease: "easeInOut" }}
      >
        {spinning ? "Spinning..." : selectedSection || "Spin Wheel"}
      </motion.div>
      <Button onClick={spinWheel} className="mb-4 bg-green-500 hover:bg-green-600" disabled={spinning}>
        {spinning ? "Spinning..." : "Spin to Select Section"}
      </Button>
      <div className="flex gap-4 flex-wrap max-w-screen-md justify-center">
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

