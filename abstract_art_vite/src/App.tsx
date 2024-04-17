import { createClient } from "@supabase/supabase-js";
import { useCallback, useEffect, useState } from "react";

function App() {
  const [imageIdx, setImageIdx] = useState(1);
  const supabaseUrl = import.meta.env.VITE_SUPA_URL;
  const supabaseKey = import.meta.env.VITE_SUPA_KEY;

  const supabase = useCallback(
    () => createClient(supabaseUrl, supabaseKey),
    [supabaseUrl, supabaseKey]
  );

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "ArrowRight") {
        setImageIdx((prevIdx) => prevIdx + 1);
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    // Cleanup function to remove the event listener when the component unmounts
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []); // Empty dependency array means this effect runs once on mount and cleanup on unmount

  async function insertData(
    userID: number,
    paintingID: number,
    rating: number
  ) {
    console.log(userID, paintingID, rating);
  }

  return (
    <div className="flex items-center justify-center h-screen bg-[rgb(217,217,217)]">
      {imageIdx % 3 != 0 ? (
        <img
          className="h-screen aspect-square"
          src={`./experiment/${imageIdx}.jpeg`}
          alt="experiment"
        />
      ) : (
        <SAM />
      )}
    </div>
  );
}

function SAM() {
  const sam_images = [
    "./sam/1.svg",
    "./sam/2.svg",
    "./sam/3.svg",
    "./sam/4.svg",
    "./sam/5.svg",
    "./sam/6.svg",
    "./sam/7.svg",
    "./sam/8.svg",
    "./sam/9.svg",
  ];

  return (
    <div className="flex flex-col gap-8 items-center justify-between">
      <div className="pb-16">
        <h1 className="text-2xl">
          How pleasant did you find the previous painting?
        </h1>
      </div>
      <div className="flex items-center justify-center">
        {sam_images.map((image, idx) => (
          <img key={idx} className="w-40" src={image} alt="sam" />
        ))}
      </div>
      <div className="pb-16">
        <div className="flex items-center justify-center">
          {Array.from({ length: 9 }, (_, i) => (
            <input
              key={i}
              type="radio"
              name="sam"
              value={i + 1}
              className="w-40 h-8"
            />
          ))}
        </div>
        <div className="flex text-2xl font-normal items-center justify-between pt-8">
          <span>Very unpleasant</span>

          <span>Very plesant</span>
        </div>
      </div>
      <div className="flex items-center justify-center">
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Submit
        </button>
      </div>
    </div>
  );
}
export default App;

