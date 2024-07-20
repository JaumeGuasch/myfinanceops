import {api} from "@/main"
import { useAuthStore } from "@/stores/auth";

const API_URL = import.meta.env.VITE_API_URL || process.env.VUE_APP_API_URL;

const signup = (email: string, password: string, name: string, surnames: string, organization: string) => {
    return api.post(`${API_URL}signup`, {
        email,
        password,
        name,
        surnames,
        organization,
    });
};

const login = async (email: string, password: string) => {
  const response = await api.post(`${API_URL}login`, {
    email,
    password,
  });
  console.log(response.data)
  return response.data;
};

const logout = async () => {
    return api.post(`${API_URL}logout`);

}

export default {
    signup,
    login,
    logout,
}
