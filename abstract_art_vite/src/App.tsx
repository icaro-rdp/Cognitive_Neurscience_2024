import { createClient } from "@supabase/supabase-js";
import { useCallback } from "react";

function App() {
  const supabaseUrl = import.meta.env.VITE_SUPA_URL;
  const supabaseKey = import.meta.env.VITE_SUPA_KEY;

  const supabase = useCallback(
    () => createClient(supabaseUrl, supabaseKey),
    [supabaseUrl, supabaseKey]
  );

  async function insertData(
    userID: number,
    paintingID: number,
    rating: number
  ) {
    console.log(userID, paintingID, rating);
    console.log(supabase());
    // const { data, error } = await supabase()
    //   .from("SAM")
    //   .insert({ userID: userID, paintingID: paintingID, rating: rating });
    // console.log(data, error);
  }

  return (
    <>
      <button onClick={() => insertData(1, 1, 5)}>Insert Data</button>
    </>
  );
}

export default App;

