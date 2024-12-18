import { createBrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import Repository from "./Components/Repository.jsx";
import SpeechAnalysis from "./Components/SpeechAnalysis.jsx";
import Ai_therapist from "./Components/Ai_therapist.jsx";
import "./index.css"

const router = createBrowserRouter([
{
    path: "/",
    element: <App />,
},
{
    path: "/repository",
    element: <Repository />,
},
{
    path: "/speech_analysis",
    element: <SpeechAnalysis />,
},
{
    path: "/ai_therapist",
    element: <Ai_therapist />,
}
]);

export default router;