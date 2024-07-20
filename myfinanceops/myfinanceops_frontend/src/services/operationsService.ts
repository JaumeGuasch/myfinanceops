import {api} from "@/main";

const API_URL = import.meta.env.VITE_API_URL || process.env.VUE_APP_API_URL;

const getOperations = async () => {
    try {
        const response = await api.get(`${API_URL}operations`);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error("Error fetching operations");
    }
};

export default {
    getOperations,
};