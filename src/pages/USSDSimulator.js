import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  Phone,
  Send,
  MessageSquare,
  ArrowLeft,
  Home,
  BookOpen,
  Calendar,
  HelpCircle,
  Users,
} from "lucide-react";

const USSDSimulator = () => {
  const [phoneNumber, setPhoneNumber] = useState("+254712345678");
  const [currentScreen, setCurrentScreen] = useState("home");
  const [userInput, setUserInput] = useState("");
  const [sessionHistory, setSessionHistory] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  const ussdMenu = {
    home: {
      title: "MaktabaAI - Digital Library",
      message:
        "Welcome to MaktabaAI! Choose an option:\n1. Search Book\n2. Request Summary\n3. Reserve Book\n4. Revision Materials\n5. Ask Librarian\n6. Career & STEM Guidance",
      options: ["1", "2", "3", "4", "5", "6"],
    },
    search: {
      title: "Search Book",
      message: "Enter book title or keywords:",
      input: true,
    },
    summary: {
      title: "Request Summary",
      message: "Enter book title for summary:",
      input: true,
    },
    reserve: {
      title: "Reserve Book",
      message: "Enter book title to reserve:",
      input: true,
    },
    revision: {
      title: "Revision Materials",
      message:
        "Select subject:\n1. Mathematics\n2. Physics\n3. Chemistry\n4. Biology\n5. English\n6. History",
      options: ["1", "2", "3", "4", "5", "6"],
    },
    librarian: {
      title: "Ask Librarian",
      message: "Type your academic question:",
      input: true,
    },
    stem: {
      title: "Career & STEM Guidance",
      message:
        "Choose guidance area:\n1. Career Information\n2. STEM Role Models\n3. Scholarship Info\n4. Study Tips\n5. Mentorship Programs",
      options: ["1", "2", "3", "4", "5"],
    },
  };

  const handleConnect = () => {
    setIsConnected(true);
    setCurrentScreen("home");
    setSessionHistory([
      {
        type: "system",
        message: "Connecting to MaktabaAI...",
        timestamp: new Date(),
      },
    ]);

    setTimeout(() => {
      setSessionHistory((prev) => [
        ...prev,
        {
          type: "system",
          message: ussdMenu.home.message,
          timestamp: new Date(),
        },
      ]);
    }, 1000);
  };

  const handleDisconnect = () => {
    setIsConnected(false);
    setCurrentScreen("home");
    setSessionHistory([]);
    setUserInput("");
  };

  const handleInput = (input) => {
    if (!input.trim()) return;

    const newEntry = {
      type: "user",
      message: input,
      timestamp: new Date(),
    };

    setSessionHistory((prev) => [...prev, newEntry]);

    // Process the input based on current screen
    setTimeout(() => {
      let response = "";

      if (currentScreen === "home") {
        switch (input) {
          case "1":
            setCurrentScreen("search");
            response = ussdMenu.search.message;
            break;
          case "2":
            setCurrentScreen("summary");
            response = ussdMenu.summary.message;
            break;
          case "3":
            setCurrentScreen("reserve");
            response = ussdMenu.reserve.message;
            break;
          case "4":
            setCurrentScreen("revision");
            response = ussdMenu.revision.message;
            break;
          case "5":
            setCurrentScreen("librarian");
            response = ussdMenu.librarian.message;
            break;
          case "6":
            setCurrentScreen("stem");
            response = ussdMenu.stem.message;
            break;
          default:
            response = "Invalid option. Please try again.";
        }
      } else if (currentScreen === "search") {
        response = `Searching for "${input}"...\n\nFound 3 results:\n1. Introduction to ${input} - Available\n2. Advanced ${input} - Reserved\n3. ${input} for Beginners - Available\n\nReply with book number to view details.`;
      } else if (currentScreen === "summary") {
        response = `Sending summary of "${input}" via SMS...\n\nSummary will arrive in 2-3 minutes. Key topics include main concepts, important formulas, and exam tips.`;
      } else if (currentScreen === "reserve") {
        response = `Book "${input}" reserved successfully!\n\nReservation ID: RES${Math.floor(Math.random() * 10000)}\nDue date: 7 days from today\nSMS confirmation sent to ${phoneNumber}`;
      } else if (currentScreen === "revision") {
        const subjects = {
          1: "Mathematics",
          2: "Physics",
          3: "Chemistry",
          4: "Biology",
          5: "English",
          6: "History",
        };
        response = `Sending ${subjects[input] || "selected"} revision materials via SMS...\n\nTopics: Key concepts, practice questions, and exam preparation tips.`;
      } else if (currentScreen === "librarian") {
        response = `Processing your question: "${input}"\n\nOur AI librarian is preparing a detailed answer. You'll receive it via SMS shortly.`;
      } else if (currentScreen === "stem") {
        const stemOptions = {
          1: "Career Information",
          2: "STEM Role Models",
          3: "Scholarship Info",
          4: "Study Tips",
          5: "Mentorship Programs",
        };
        response = `Loading ${stemOptions[input] || "selected"} content...\n\nInformation will be sent via SMS with detailed resources and contacts.`;
      } else {
        response = "Processing your request...";
      }

      setSessionHistory((prev) => [
        ...prev,
        {
          type: "system",
          message: response,
          timestamp: new Date(),
        },
      ]);
    }, 1000);

    setUserInput("");
  };

  const handleBack = () => {
    if (currentScreen !== "home") {
      setCurrentScreen("home");
      setSessionHistory((prev) => [
        ...prev,
        {
          type: "system",
          message: ussdMenu.home.message,
          timestamp: new Date(),
        },
      ]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">USSD Simulator</h1>
          <p className="mt-2 text-gray-600">
            Test the MaktabaAI USSD interface
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={isConnected ? handleDisconnect : handleConnect}
            className={`btn px-6 py-2 ${
              isConnected
                ? "bg-red-600 hover:bg-red-700 text-white"
                : "btn-primary"
            }`}
          >
            <Phone className="h-4 w-4 mr-2" />
            {isConnected ? "Disconnect" : "Connect"}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Phone Simulator */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">
              Phone Simulator
            </h2>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">
                {isConnected ? "Connected" : "Disconnected"}
              </span>
            </div>
          </div>

          {/* Phone Frame */}
          <div className="bg-gray-900 rounded-2xl p-4 mx-auto max-w-sm">
            <div className="bg-black rounded-xl p-4">
              {/* Phone Status Bar */}
              <div className="flex justify-between items-center mb-4 text-white text-xs">
                <span>{phoneNumber}</span>
                <div className="flex items-center space-x-1">
                  <div className="w-4 h-3 border border-white rounded-sm">
                    <div className="w-full h-full bg-white rounded-sm scale-x-75 origin-left"></div>
                  </div>
                </div>
              </div>

              {/* USSD Screen */}
              <div className="bg-green-950 text-green-400 p-4 rounded-lg min-h-[300px] font-mono text-sm">
                {isConnected ? (
                  <div className="space-y-2">
                    {sessionHistory.map((entry, index) => (
                      <div key={index} className="space-y-1">
                        {entry.type === "system" ? (
                          <div className="whitespace-pre-line">
                            {entry.message}
                          </div>
                        ) : (
                          <div className="text-green-300">
                            &gt; {entry.message}
                          </div>
                        )}
                      </div>
                    ))}

                    {currentScreen !== "home" && (
                      <div className="pt-2 border-t border-green-800 text-xs">
                        0. Back
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="flex items-center justify-center h-[300px]">
                    <div className="text-center">
                      <Phone className="h-8 w-8 mx-auto mb-2 opacity-50" />
                      <p className="text-xs opacity-75">
                        Press Connect to start
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Input Area */}
              {isConnected && (
                <div className="mt-4 space-y-2">
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={userInput}
                      onChange={(e) => setUserInput(e.target.value)}
                      onKeyPress={(e) =>
                        e.key === "Enter" && handleInput(userInput)
                      }
                      placeholder="Enter option or text"
                      className="flex-1 bg-gray-800 text-white px-3 py-2 rounded text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                    />
                    <button
                      onClick={() => handleInput(userInput)}
                      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm"
                    >
                      <Send className="h-4 w-4" />
                    </button>
                  </div>

                  {/* Quick Options */}
                  {ussdMenu[currentScreen]?.options && (
                    <div className="grid grid-cols-3 gap-2">
                      {ussdMenu[currentScreen].options.map((option) => (
                        <button
                          key={option}
                          onClick={() => handleInput(option)}
                          className="bg-gray-800 hover:bg-gray-700 text-white py-1 rounded text-xs"
                        >
                          {option}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Session Info */}
        <div className="space-y-6">
          <div className="card p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Session Details
            </h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">
                  Phone Number
                </label>
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  className="input mt-1"
                  placeholder="+254712345678"
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600">
                  Current Screen
                </label>
                <div className="mt-1 p-2 bg-gray-50 rounded text-sm">
                  {ussdMenu[currentScreen]?.title || "Disconnected"}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600">
                  Session Duration
                </label>
                <div className="mt-1 p-2 bg-gray-50 rounded text-sm">
                  {isConnected ? "00:00:00" : "Not connected"}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-600">
                  Messages Exchanged
                </label>
                <div className="mt-1 p-2 bg-gray-50 rounded text-sm">
                  {sessionHistory.length} messages
                </div>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Quick Test Scenarios
            </h2>
            <div className="space-y-2">
              <button
                onClick={() => {
                  handleConnect();
                  setTimeout(() => handleInput("1"), 2000);
                  setTimeout(() => handleInput("physics"), 4000);
                }}
                className="w-full btn btn-outline py-2 text-left"
              >
                <BookOpen className="h-4 w-4 mr-2 inline" />
                Test Book Search
              </button>

              <button
                onClick={() => {
                  handleConnect();
                  setTimeout(() => handleInput("2"), 2000);
                  setTimeout(() => handleInput("chemistry basics"), 4000);
                }}
                className="w-full btn btn-outline py-2 text-left"
              >
                <MessageSquare className="h-4 w-4 mr-2 inline" />
                Test Summary Request
              </button>

              <button
                onClick={() => {
                  handleConnect();
                  setTimeout(() => handleInput("5"), 2000);
                  setTimeout(
                    () => handleInput("What is photosynthesis?"),
                    4000,
                  );
                }}
                className="w-full btn btn-outline py-2 text-left"
              >
                <HelpCircle className="h-4 w-4 mr-2 inline" />
                Test Ask Librarian
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default USSDSimulator;
