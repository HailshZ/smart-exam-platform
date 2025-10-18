import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ToastContainer } from 'react-toastify';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

// Components
import Navbar from './components/Common/Navbar';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import AdminDashboard from './components/Admin/AdminDashboard';
import TeacherDashboard from './components/Teacher/TeacherDashboard';
import StudentDashboard from './components/Student/StudentDashboard';
import ExamInterface from './components/Exam/ExamInterface';
import LoadingSpinner from './components/Common/LoadingSpinner';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <AppContent />
          <ToastContainer position="top-right" autoClose={5000} />
        </div>
      </Router>
    </AuthProvider>
  );
}

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <>
      <Navbar />
      <main className="container-fluid px-0">
        <Routes>
          <Route 
            path="/login" 
            element={!user ? <Login /> : <Navigate to={`/${user.role}`} />} 
          />
          <Route 
            path="/register" 
            element={!user ? <Register /> : <Navigate to={`/${user.role}`} />} 
          />
          <Route 
            path="/admin/*" 
            element={user?.role === 'admin' ? <AdminDashboard /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/teacher/*" 
            element={user?.role === 'teacher' ? <TeacherDashboard /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/student/*" 
            element={user?.role === 'student' ? <StudentDashboard /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/exam/:examId" 
            element={user?.role === 'student' ? <ExamInterface /> : <Navigate to="/login" />} 
          />
          <Route path="/" element={<Navigate to={user ? `/${user.role}` : '/login'} />} />
        </Routes>
      </main>
    </>
  );
}

export default App;