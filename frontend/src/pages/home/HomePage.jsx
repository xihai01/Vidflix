import React from 'react'
import AuthScreen from './AuthScreen'
import HomeScreen from './HomeScreen'
import { useAuthStore } from '../../store/authUser'

const HomePage = () => {
  const { isSignedIn } = useAuthStore();

  return (
    <div>{isSignedIn ? <HomeScreen /> : <AuthScreen />}</div>
  )
}

export default HomePage