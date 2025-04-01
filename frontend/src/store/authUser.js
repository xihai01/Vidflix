import axios from "axios";
import toast from "react-hot-toast";
import { create } from "zustand";

export const useAuthStore = create((set) => ({
  user: null,
  isSigningUp: false,
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
      set({ user: response.data.user, isSigningUp: false });
      toast.success("Account created successfully");
    } catch(error) {
      console.log(error);
      toast.error(error.response.data.error || "An error occurred");
      set({ isSigningUp: false, user: null });
    }
  },
  login: async () => {},
  logout: async () => {},
  authCheck: async () => {},
}));
