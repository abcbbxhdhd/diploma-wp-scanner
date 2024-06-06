import { DarkThemeToggle } from "flowbite-react";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import InitiateScanPage from "./components/InitiateScanPage";
import ViewScanPage from "./components/ViewScanPage";
import ViewAllScansPage from "./components/ViewAllScansPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<InitiateScanPage />}/>
        <Route path="/scans/initiate" element={<InitiateScanPage />}/>
        <Route path="/scans/view/:scanId" element={<ViewScanPage/>} />
        <Route path="/scans/list" element={<ViewAllScansPage/>} />
      </Routes>
    </Router>
  );
}

export default App;
