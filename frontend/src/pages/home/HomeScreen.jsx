import React from "react";
import { useAuthStore } from "../../store/authUser";

const HomeScreen = () => {
  const { user, logout } = useAuthStore();
  console.log("the access token on home screen is", user.access_token)
  return (
    <div>
      HomeScreen
      <button onClick={() => logout(user.access_token)}>logout</button>
    </div>
  );
};

export default HomeScreen;
