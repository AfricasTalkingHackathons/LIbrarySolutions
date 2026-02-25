import React from "react";
import { motion } from "framer-motion";
import {
  Users,
  BookOpen,
  Phone,
  Calendar,
  TrendingUp,
  Activity,
  Globe,
  Smartphone,
} from "lucide-react";

const Dashboard = () => {
  const stats = [
    {
      title: "Total Users",
      value: "12,543",
      change: "+12.5%",
      icon: Users,
      color: "bg-blue-500",
      bgColor: "bg-blue-50",
    },
    {
      title: "Books Available",
      value: "3,847",
      change: "+8.2%",
      icon: BookOpen,
      color: "bg-green-500",
      bgColor: "bg-green-50",
    },
    {
      title: "USSD Sessions",
      value: "45,678",
      change: "+23.1%",
      icon: Phone,
      color: "bg-purple-500",
      bgColor: "bg-purple-50",
    },
    {
      title: "Active Reservations",
      value: "892",
      change: "+5.4%",
      icon: Calendar,
      color: "bg-orange-500",
      bgColor: "bg-orange-50",
    },
  ];

  const recentActivity = [
    {
      id: 1,
      user: "John Doe",
      action: 'Reserved "Introduction to Physics"',
      time: "2 mins ago",
      type: "reservation",
    },
    {
      id: 2,
      user: "Jane Smith",
      action: 'Searched for "Mathematics"',
      time: "5 mins ago",
      type: "search",
    },
    {
      id: 3,
      user: "Mike Johnson",
      action: "Requested book summary",
      time: "12 mins ago",
      type: "summary",
    },
    {
      id: 4,
      user: "Sarah Williams",
      action: "Asked academic question",
      time: "18 mins ago",
      type: "question",
    },
  ];

  const features = [
    {
      title: "USSD Access",
      description: "Dial *789*5960# to access library services",
      icon: Smartphone,
      color: "text-primary-600",
      bgColor: "bg-primary-50",
    },
    {
      title: "SMS Notifications",
      description: "Receive book summaries and reminders",
      icon: Phone,
      color: "text-secondary-600",
      bgColor: "bg-secondary-50",
    },
    {
      title: "Multi-Language Support",
      description: "Available in English, Swahili, Luganda",
      icon: Globe,
      color: "text-accent-600",
      bgColor: "bg-accent-50",
    },
    {
      title: "Real-time Analytics",
      description: "Track usage and engagement metrics",
      icon: TrendingUp,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Welcome to MaktabaAI Digital Library Platform
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button className="btn btn-primary px-6 py-2">
            <Activity className="h-4 w-4 mr-2" />
            View Live Status
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="card p-6 hover:shadow-lg transition-shadow duration-300"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    {stat.title}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">
                    {stat.value}
                  </p>
                  <div className="flex items-center mt-2">
                    <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                    <span className="text-sm text-green-600 font-medium">
                      {stat.change}
                    </span>
                  </div>
                </div>
                <div className={`${stat.bgColor} p-3 rounded-lg`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Platform Features
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className={`${feature.bgColor} p-2 rounded-lg`}>
                    <Icon className={`h-5 w-5 ${feature.color}`} />
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {feature.description}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>

        <div className="card p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Recent Activity
          </h2>
          <div className="space-y-3">
            {recentActivity.map((activity, index) => (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      activity.type === "reservation"
                        ? "bg-blue-500"
                        : activity.type === "search"
                          ? "bg-green-500"
                          : activity.type === "summary"
                            ? "bg-purple-500"
                            : "bg-orange-500"
                    }`}
                  />
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {activity.user}
                    </p>
                    <p className="text-xs text-gray-600">{activity.action}</p>
                  </div>
                </div>
                <span className="text-xs text-gray-500">{activity.time}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <button className="btn btn-outline py-3">
            <Phone className="h-4 w-4 mr-2" />
            Test USSD
          </button>
          <button className="btn btn-outline py-3">
            <BookOpen className="h-4 w-4 mr-2" />
            Add Book
          </button>
          <button className="btn btn-outline py-3">
            <Users className="h-4 w-4 mr-2" />
            View Users
          </button>
          <button className="btn btn-outline py-3">
            <Calendar className="h-4 w-4 mr-2" />
            Manage Reservations
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
