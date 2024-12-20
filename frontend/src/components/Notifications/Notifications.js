import React, { useEffect, useState, useCallback } from "react";
import { getToken } from "../../utils/auth";
import axios from "axios";

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");

  const token = getToken();
  const host = window.location.hostname;

  // Wrap fetchNotifications in useCallback
  const fetchNotifications = useCallback(async () => {
    try {
      const response = await axios.get(
        `http://${host}:8000/api/notifications`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // Normalize API notifications structure
      const apiNotifications = response.data.map((notif) => ({
        ...notif,
        id: notif.id || Math.random().toString(36).substr(2, 9), // Generate a unique id if missing
      }));

      setNotifications(apiNotifications);
    } catch (error) {
      console.error("Error fetching notifications:", error);
    }
  }, [host, token]); // Dependencies for useCallback

  useEffect(() => {
    fetchNotifications();

    const wsUrl = `ws://${host}:8000/ws/notifications/?token=${token}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => console.log("WebSocket connection established");
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // Normalize WebSocket notifications structure
        const wsNotification = {
          id: data.id,
          message: data.message.message,
          timestamp: data.message.created_at,
          read: data.message.read,
        };

        setNotifications((prev) => [...prev, wsNotification]);
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };
    ws.onclose = () => console.log("WebSocket connection closed");

    return () => ws.close();
  }, [fetchNotifications, host, token]); // Dependencies for useEffect

  // Search for notifications
  const searchNotifications = async () => {
    if (searchQuery) {
      try {
        const response = await axios.get(
          `http://${host}:8000/search/notifications/`,
          {
            params: { q: searchQuery },
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setNotifications(response.data);
      } catch (error) {
        console.error("Error searching notifications:", error);
      }
    } else {
      fetchNotifications();
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Notifications</h2>

      {/* Search Input */}
      <div className="mb-4">
        <input
          type="text"
          className="w-full p-2 border border-gray-300 rounded"
          placeholder="Search notifications..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button
          onClick={searchNotifications}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Search
        </button>
      </div>

      {notifications.length > 0 ? (
        <ul className="space-y-4">
          {notifications.map((notif) => (
            <li
              key={notif.id}
              className="p-4 bg-gray-100 rounded-lg shadow-sm flex items-center justify-between"
            >
              <div className="text-lg font-semibold text-gray-700">
                {notif.message}
              </div>
              <div className="ml-4 flex items-center justify-end gap-5">
                <div className="text-sm text-gray-500 mt-1">
                  <span className="font-medium">Time:</span>{" "}
                  {notif.timestamp
                    ? new Date(notif.timestamp).toLocaleString()
                    : "Dec. 15, 2024, 11:46 p.m."}
                </div>
                <div
                  className={`text-sm mt-1 font-medium ${
                    notif.read ? "text-green-600" : "text-red-600"
                  }`}
                >
                  {notif.read ? "Read" : "Unread"}
                </div>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-gray-500 text-center">
          No notifications available.
        </div>
      )}
    </div>
  );
};

export default Notifications;
