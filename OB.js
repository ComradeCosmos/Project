import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

const getRandomTile = () => Math.floor(Math.random() * 100) + 1;

export default function RandomTiles() {
  const [tiles, setTiles] = useState([]);

  const drawTile = () => {
    if (tiles.length < 6) {
      setTiles((prevTiles) => [...prevTiles, getRandomTile()]);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
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
        disabled={tiles.length >= 6}
      >
        {tiles.length >= 6 ? "Limit Reached" : "Draw Tile"}
      </Button>
    </div>
  );
}
