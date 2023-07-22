import React, { createContext, useState, useEffect } from 'react';
import {fetchLoginUser, handleLogout, fetchUserInformation, fetchCreateUser } from '../api/fetchUser.js'


export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const getUser = async () => {
      try {
        const token = localStorage.getItem('token'); // Assuming you're storing the JWT token in localStorage
        if (!token) {
          return;
        }

        const response = await fetchUserInformation()
        if (response.ok) {
            const data = response.json()
            setCurrentUser(data)
        }

      } catch (error) {
        setCurrentUser(null)
        console.error(error);
      }
    };
    getUser();
  }, []);

  const login = async (phone, password) => {
    const response = await fetchLoginUser(phone, password)
    if (response.ok){
        const data = await response.json()
        setCurrentUser(data)
        return
    } else {
        setCurrentUser(null)
    }
  }

  const logout = () => {
    handleLogout()
    setCurrentUser(null)
  }

  const createUser = async (phoneNumber, firstName, lastName, password) => {
    const response = await fetchCreateUser(
        phoneNumber, firstName, lastName, password
    )
    return response
  } 



  // Then provide the current user in the context
  return (
    <AuthContext.Provider value={{currentUser, login, logout, createUser}}>
      {children}
    </AuthContext.Provider>
  );
};