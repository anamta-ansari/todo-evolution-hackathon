'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import {
  getUserTasks,
  createUserTask,
  updateUserTask,
  deleteUserTask,
  toggleTaskCompletion
} from '@/utils/api';

// Define the Task type
type Task = {
  id: number;
  title: string;
  description: string;
  completed: boolean;
};

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<number | null>(null); // Track loading state for individual actions
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);
  const router = useRouter();
  const { user, signOut, isLoading } = useAuth();

  // Calculate stats
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const overdueTasks = 0; // Placeholder - implement due date logic if needed

  // Calculate completion percentage
  const completionPercentage = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Protect the route - redirect to signin if not authenticated
  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/signin');
    }
  }, [user, isLoading, router]);

  // Load tasks on component mount
  useEffect(() => {
    if (!user && !isLoading) {
      router.push('/signin');
      return;
    }

    if (user) {
      const fetchTasks = async () => {
        try {
          setLoading(true);
          const tasksFromApi = await getUserTasks(user.id);
          setTasks(tasksFromApi);
        } catch (err) {
          setError('Failed to load tasks');
          console.error('Error loading tasks:', err);
        } finally {
          setLoading(false);
        }
      };

      fetchTasks();
    }
  }, [user, isLoading, router]);

  // Clear success message after 3 seconds
  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => {
        setSuccess(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [success]);

  // Handle logout
  const handleLogout = async () => {
    try {
      await signOut();
      router.push('/signin');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  // Create a new task
  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || !user) return;

    try {
      const newTask = await createUserTask(user.id, { title, description });
      setTasks([...tasks, newTask]);
      setTitle('');
      setDescription('');
      setSuccess('Task added successfully!');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      console.error('Error creating task:', err);
      setSuccess(null);
    }
  };

  // Update an existing task
  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!editingTask || !title.trim() || !user) return;

    try {
      setActionLoading(editingTask.id);
      const updatedTask = await updateUserTask(user.id, editingTask.id, {
        title: title,
        description: description
      });

      setTasks(tasks.map(task =>
        task.id === editingTask.id ? updatedTask : task
      ));

      setEditingTask(null);
      setTitle('');
      setDescription('');
      setSuccess('Task updated successfully!');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      console.error('Error updating task:', err);
      setSuccess(null);
    } finally {
      setActionLoading(null);
    }
  };

  // Delete a task
  const handleDeleteTask = async (id: number) => {
    if (!user) return;

    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        setActionLoading(id);
        await deleteUserTask(user.id, id);
        setTasks(tasks.filter(task => task.id !== id));
        setSuccess('Task deleted successfully!');
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to delete task');
        console.error('Error deleting task:', err);
        setSuccess(null);
      } finally {
        setActionLoading(null);
      }
    }
  };

  // Toggle task completion status
  const toggleComplete = async (id: number) => {
    if (!user) return;

    try {
      setActionLoading(id);
      const updatedTask = await toggleTaskCompletion(user.id, id);

      // Optimistic update: update the local state immediately
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));

      // Re-fetch the full task list to ensure accurate counts and consistency with backend
      const refreshedTasks = await getUserTasks(user.id);
      setTasks(refreshedTasks);

      setSuccess(updatedTask.completed ? 'Task marked as complete!' : 'Task marked as incomplete!');
      setError(null);
    } catch (err: any) {
      // If there's an error, revert the optimistic update by re-fetching
      try {
        const refreshedTasks = await getUserTasks(user.id);
        setTasks(refreshedTasks);
      } catch (revertErr) {
        console.error('Error reverting task after failed update:', revertErr);
      }

      setError(err.message || 'Failed to update task status');
      console.error('Error toggling task completion:', err);
      setSuccess(null);
    } finally {
      setActionLoading(null);
    }
  };

  // Prepare for editing a task
  const startEditing = (task: Task) => {
    setEditingTask(task);
    setTitle(task.title);
    setDescription(task.description || '');
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingTask(null);
    setTitle('');
    setDescription('');
  };

  // Show loading state if auth is still loading
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 to-purple-100">
        <p className="text-xl">Loading...</p>
      </div>
    );
  }

  // Show nothing if not authenticated (will redirect)
  if (!user && !isLoading) {
    return null;
  }

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-pink-50 to-purple-100">
      {/* Sidebar */}
      <aside className={`bg-white shadow-lg transform transition-transform duration-300 ease-in-out z-10 fixed md:relative h-100vh w-64 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0`}>
        <div className="p-6 border-b border-pink-100">
          <div className="flex items-center">
            <div className="w-10 h-10 rounded-full bg-pink-500 flex items-center justify-center text-white mr-3">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-pink-600">TodoHub</h1>
          </div>
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            <li>
              <Link href="/dashboard" className="flex items-center p-3 text-gray-700 hover:bg-pink-50 rounded-lg transition-colors">
                <svg className="w-5 h-5 mr-3 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                </svg>
                Dashboard
              </Link>
            </li>
            <li>
              <Link href="/dashboard" className="flex items-center p-3 bg-pink-50 text-pink-600 font-medium rounded-lg">
                <svg className="w-5 h-5 mr-3 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                My Tasks
              </Link>
            </li>
            <li>
              <Link href="#" className="flex items-center p-3 text-gray-700 hover:bg-pink-50 rounded-lg transition-colors">
                <svg className="w-5 h-5 mr-3 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
                </svg>
                Categories
              </Link>
            </li>
            <li>
              <Link href="#" className="flex items-center p-3 text-gray-700 hover:bg-pink-50 rounded-lg transition-colors">
                <svg className="w-5 h-5 mr-3 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                Calendar
              </Link>
            </li>
            <li>
              <Link href="#" className="flex items-center p-3 text-gray-700 hover:bg-pink-50 rounded-lg transition-colors">
                <svg className="w-5 h-5 mr-3 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
                Analytics
              </Link>
            </li>
            <li>
              <Link href="/settings" className="flex items-center p-3 text-gray-700 hover:bg-pink-50 rounded-lg transition-colors">
                <svg className="w-5 h-5 mr-3 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                Settings
              </Link>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white shadow-sm z-10 h-16">
          <div className="flex items-center justify-between p-4">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden mr-4 text-gray-500 focus:outline-none"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              </button>
              {/* <div className="flex items-center">
                <h1 className="text-xl font-bold text-pink-600">TodoHub</h1>
              </div> */}
            </div>
            <div className="flex items-center space-x-4">
              {/* Profile dropdown */}
              <div className="relative">
                <button
                  onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                  className="flex items-center space-x-2 focus:outline-none"
                >
                  <img
                    src={user?.avatar || "https://ui-avatars.com/api/?name="+encodeURIComponent(user?.name || "User")}
                    alt="Profile"
                    className="w-10 h-10 rounded-full border-2 border-pink-200"
                  />
                  <span className="hidden md:inline-block text-gray-700">{user?.name}</span>
                  <svg
                    className={`w-4 h-4 text-gray-500 transition-transform duration-200 ${profileDropdownOpen ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </button>

                {profileDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20 border border-gray-200">
                    <Link
                      href="/settings"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-pink-50 hover:text-pink-600"
                      onClick={() => setProfileDropdownOpen(false)}
                    >
                      Settings
                    </Link>
                    <button
                      onClick={() => {
                        handleLogout();
                        setProfileDropdownOpen(false);
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-pink-50 hover:text-pink-600"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6 bg-gradient-to-br from-pink-50 to-purple-100">
          {/* Welcome Section */}
          <section className="mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Welcome back, {user?.name}</h1>
            <p className="text-gray-600">Here's what's on your plate today</p>
          </section>

          {/* Stats Cards */}
          <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center">
                <div className="p-3 rounded-lg bg-pink-100 text-pink-600 mr-4">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                </div>
                <div>
                  <p className="text-gray-500">Total Tasks</p>
                  <p className="text-2xl font-bold text-gray-800">{totalTasks}</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center">
                <div className="p-3 rounded-lg bg-yellow-100 text-yellow-600 mr-4">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div>
                  <p className="text-gray-500">Pending Tasks</p>
                  <p className="text-2xl font-bold text-gray-800">{pendingTasks}</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="flex items-center">
                <div className="p-3 rounded-lg bg-green-100 text-green-600 mr-4">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div>
                  <p className="text-gray-500">Completed Tasks</p>
                  <p className="text-2xl font-bold text-gray-800">{completedTasks}</p>
                </div>
              </div>
            </div>
          </section>

          {/* Today's Tasks and Add Task Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Today's Tasks */}
            <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-md">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-gray-800">Today's Tasks</h2>
                <button className="text-pink-500 hover:text-pink-700">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path>
                  </svg>
                </button>
              </div>

              {loading ? (
                <div className="flex justify-center items-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-pink-500"></div>
                </div>
              ) : tasks.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No tasks for today. Add your first task!</p>
              ) : (
                <div className="space-y-4">
                  {tasks.map((task) => (
                    <div
                      key={task.id}
                      className={`p-4 border rounded-lg flex items-start ${
                        task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => toggleComplete(task.id)}
                        className="mt-1 h-5 w-5 text-pink-600 rounded focus:ring-pink-500"
                      />
                      <div className="ml-4 flex-1">
                        <div className="flex justify-between">
                          <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                            {task.title}
                          </h3>
                          <span className="text-gray-500 text-sm">10:00 AM</span>
                        </div>
                        <p className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-600'} mt-1`}>
                          {task.description}
                        </p>
                        <div className="mt-2">
                          <span className="inline-block px-2 py-1 text-xs font-semibold text-pink-700 bg-pink-100 rounded-full">
                            {task.title.includes('Design') ? 'Design' : task.title.includes('Meeting') ? 'Meeting' : 'Personal'}
                          </span>
                        </div>
                      </div>
                      <div className="flex space-x-2 ml-4">
                        <button
                          onClick={() => startEditing(task)}
                          disabled={actionLoading === task.id}
                          className="p-2 text-gray-500 hover:text-pink-600 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                          </svg>
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          disabled={actionLoading === task.id}
                          className="p-2 text-gray-500 hover:text-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Add Task Section */}
            <div className="bg-white p-6 rounded-xl shadow-md">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Add New Task</h2>

              <form onSubmit={editingTask ? handleUpdateTask : handleCreateTask}>
                <div className="mb-4">
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
                    placeholder="Enter a task..."
                    required
                  />
                </div>

                <div className="flex items-center justify-between">
                  <button
                    type="button"
                    className="p-2 text-gray-500 hover:text-pink-600"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                  </button>

                  <button
                    type="submit"
                    disabled={actionLoading !== null}
                    className={`px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors ${
                      actionLoading !== null ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                  >
                    {editingTask ? 'Update Task' : 'Add Task'}
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Inspirational Quote */}
          <section className="bg-white p-6 rounded-xl shadow-md mb-8">
            <div className="flex items-start">
              <div className="mr-4 text-pink-500">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                </svg>
              </div>
              <div>
                <p className="text-gray-700 italic">
                  "The best way to get things done is to begin. – Lucille Ball"
                </p>
                <p className="mt-4 text-right text-gray-500">Stay motivated and keep moving forward!</p>
              </div>
            </div>
          </section>

          {/* Success message */}
          {success && (
            <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-lg">
              {success}
            </div>
          )}

          {/* Error message */}
          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {/* Tasks List - Hidden for now since we're showing Today's Tasks above */}
          <div className="hidden bg-white p-6 rounded-xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-6">Your Tasks</h2>

            {loading ? (
              <div className="flex justify-center items-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-pink-500"></div>
              </div>
            ) : tasks.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No tasks yet. Add your first task!</p>
            ) : (
              <div className="space-y-4">
                {tasks.map((task) => (
                  <div
                    key={task.id}
                    className={`p-4 border rounded-lg flex justify-between items-start ${
                      task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
                    }`}
                  >
                    <div>
                      <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : ''}`}>
                        {task.title}
                      </h3>
                      <p className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-600'} mt-1`}>
                        {task.description}
                      </p>
                    </div>

                    <div className="flex space-x-2">
                      <button
                        onClick={() => toggleComplete(task.id)}
                        disabled={actionLoading === task.id}
                        className={`p-2 rounded-full ${
                          task.completed
                            ? 'bg-green-100 text-green-600'
                            : 'bg-gray-100 text-gray-400'
                        } ${actionLoading === task.id ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80'}`}
                        aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
                      >
                        {actionLoading === task.id ? (
                          <svg className="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                        ) : task.completed ? (
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                        ) : (
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        )}
                      </button>

                      <button
                        onClick={() => startEditing(task)}
                        disabled={actionLoading === task.id}
                        className="px-3 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Edit
                      </button>

                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        disabled={actionLoading === task.id}
                        className="px-3 py-1 bg-red-100 text-red-800 rounded hover:bg-red-200 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>

        <footer className="py-4 text-center text-gray-600 text-sm">
          <p>© 2026 TodoHub. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
}