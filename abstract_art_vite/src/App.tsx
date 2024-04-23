import { createClient } from "@supabase/supabase-js";
import { useEffect, useState } from "react";

const supabaseUrl = import.meta.env.VITE_SUPA_URL;
const supabaseKey = import.meta.env.VITE_SUPA_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

function App() {
  const [imageIdx, setImageIdx] = useState(1);
  const [userID, setUserID] = useState<number>(0);
  const [state, setState] = useState<"registering" | "looking" | "rating">(
    "registering"
  );

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (state !== "looking") return;
      if (event.key === "ArrowRight") {
        setImageIdx(imageIdx + 1);
        if (imageIdx % 2 === 0) {
          setState("rating");
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    // Cleanup function to remove the event listener when the component unmounts
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [imageIdx, state]);

  return (
    <div className="flex items-center justify-center h-screen bg-[rgb(217,217,217)]">
      {state === "registering" ? (
        <>
          <input
            onChange={(e) => setUserID(parseInt(e.target.value))}
            type="number"
            placeholder="Enter your user ID"
            className="w-64 h-8 m-2 px-2 rounded border-0 border-gray-300 focus:outline-none focus:border-blue-500"
          />
          <button
            onClick={() => setState("looking")}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-4 rounded"
          >
            Submit
          </button>
        </>
      ) : (
        <Experiment
          userID={userID}
          imageIdx={imageIdx}
          state={state}
          setState={setState}
        />
      )}
    </div>
  );
}

function Experiment({
  imageIdx,
  userID,
  state,
  setState,
}: {
  userID: number;
  imageIdx: number;
  state: "registering" | "looking" | "rating";
  setState: (state: "registering" | "looking" | "rating") => void;
}) {
  return (
    <div className="flex items-center justify-center h-screen bg-[rgb(217,217,217)]">
      {state === "looking" ? (
        <img
          className="h-screen aspect-square"
          src={`./experiment/${imageIdx}.jpeg`}
          alt="experiment"
        />
      ) : (
        <>
          <SAM
            userID={userID}
            paintingID={Math.floor((imageIdx + 1) / 3)}
            setState={setState}
          />
        </>
      )}
    </div>
  );
}
interface SAMProps {
  userID: number;
  paintingID: number;
  setState?: (state: "registering" | "looking" | "rating") => void;
}

function SAM({ userID, paintingID, setState }: SAMProps) {
  const [selectedRating, setSelectedRating] = useState<number | null>(null);

  function insertData() {
    setState?.("looking");
    console.table({ userID, paintingID, selectedRating });
  }

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
          <img key={idx} className="w-32" src={image} alt="sam" />
        ))}
      </div>
      <div className="pb-16">
        <div className="flex items-center justify-center">
          {Array.from({ length: 9 }, (_, i) => (
            <input
              onChange={(e) => setSelectedRating(parseInt(e.target.value))}
              key={i}
              type="radio"
              name="sam"
              value={i + 1}
              className="w-32 h-8"
            />
          ))}
        </div>
        <div className="flex text-2xl font-normal items-center justify-between pt-8">
          <span>Very unpleasant</span>

          <span>Very pleasant</span>
        </div>
      </div>
      <div className="flex items-center justify-center">
        <button
          onClick={insertData}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Submit
        </button>
      </div>
    </div>
  );
}
export default App;

