import axios from "axios";
import toast from "react-hot-toast";
import { create } from "zustand";

export const useAuthStore = create((set) => ({
  user: null,
  isSigningUp: false,
  isLoggingOut: false,
  isLoggingIn: false,
  isSignedIn: false,
  signup: async (credentials) => {
    set({ isSigningUp: true });
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/v1/auth/register",
        credentials,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      set({ user: response.data.user, isSigningUp: false, isSignedIn: true });
      toast.success("Account created successfully");
    } catch (error) {
      console.log(error);
      toast.error(error.response.data.error || "An error occurred");
      set({ isSigningUp: false, isSignedIn: false, user: null });
    }
  },
  login: async (credentials) => {
    set({ isLoggingIn: true });
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/v1/auth/login",
        credentials,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      set({ user: response.data.user, isLoggingIn: false, isSignedIn: true });
      toast.success("Account aigned in successfully.");
    } catch (error) {
      console.log(error);
      toast.error(error.response.data.error || "An error occurred");
      set({ isLoggingIn: false, isSignedIn: false, user: null });
    }
  },
  logout: async (access_token) => {
    set({ isLoggingOut: true });
    try {
      console.log("the access token on zustand screen is", access_token)
      await axios.get("http://127.0.0.1:5000/api/v1/auth/logout", {
        headers: {
          "Authorization": "Bearer " + access_token,
        },
      });
      set({ user: null, isLoggingOut: false, isSignedIn: false });
      toast.success("Logged out successfully.");
    } catch (error) {
      set({ isLoggingOut: false, isSignedIn: true });
      toast.error(error.response.data.error || "Logout failed.");
    }
  },
}));
