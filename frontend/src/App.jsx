import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/home/HomePage";
import HomeScreen from "./pages/home/HomeScreen";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import Footer from "./components/footer";
import { Toaster } from "react-hot-toast";
import { useAuthStore } from "./store/authUser";

function App() {
  const { isSignedIn } = useAuthStore();

  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route
          path="/login"
          element={isSignedIn ? <HomeScreen /> : <LoginPage />}
        />
        <Route
          path="/signup"
          element={isSignedIn ? <HomeScreen /> : <SignUpPage />}
        />
      </Routes>
      <Footer />
      <Toaster />
    </>
  );
}

export default App;
