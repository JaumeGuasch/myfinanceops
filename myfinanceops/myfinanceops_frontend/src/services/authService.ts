import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || process.env.VUE_APP_API_URL;

const signup = (email: string, password: string, name: string, surnames: string, organization: string) => {
    return axios.post(`${API_URL}signup/`, {
        email,
        password,
        name,
        surnames,
        organization,
    });
};

const login = (email: string, password: string) => {
    return axios.post(`${API_URL}login/`, {
        email,
        password
    }).then(response => {
        console.log("login response: ", response.data);
        return response.data;
    }).catch(error => {
        console.error("Login error:", error);
        throw error;
    });
};

const logout = () => {
    // Assuming your server provides an endpoint to clear the HTTP-only cookie
    return axios.post(`${API_URL}logout/`);
};

export default {
    signup,
    login,
    logout
};