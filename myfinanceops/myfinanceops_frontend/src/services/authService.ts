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
        if (response.data.access) {
            localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
    });
};

const logout = () => {
    localStorage.removeItem('user');
};

export default {
    signup,
    login,
    logout
};