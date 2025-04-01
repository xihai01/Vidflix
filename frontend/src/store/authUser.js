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
        "http://127.0.0.1:5000/auth/register",
        credentials,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (response.status === 400) {
        toast.error(response.data.message);
      } else {
        set({ user: response.data.user, isSigningUp: false });
        toast.success("Account created successfully");
      }
    } catch {
      toast.error("An error occurred");
      set({ isSigningUp: false, user: null });
    }
  },
  login: async () => {},
  logout: async () => {},
  authCheck: async () => {},
}));
