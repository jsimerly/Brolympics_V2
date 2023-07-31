import { createContext, useState, useEffect } from 'react';
import {fetchLoginUser, handleLogout, fetchUserInformation, fetchCreateUser } from '../api/fetchUser.js'
import {getCookie} from '../api/cookies.js'


export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const getUser = async () => {
      try {
        const response = await fetchUserInformation();
        if (response.ok) {
          const data = await response.json();
          setCurrentUser(data);
        } else {
          setCurrentUser(null);
        }
      } catch (error) {
        setCurrentUser(null);
        console.error(error);
      }
    };
    getUser();
  }, []);

  const login = async (phone, password) => {
    const response = await fetchLoginUser(phone, password)
    return response
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
    <AuthContext.Provider value={{currentUser, login, logout, createUser, setCurrentUser}}>
      {children}
    </AuthContext.Provider>
  );
};