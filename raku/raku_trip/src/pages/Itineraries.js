import React, { useState } from "react";
import styles from "../styles/Itineraries.module.css";

const Itineraries = () => {
  const [tripDetails, setTripDetails] = useState({
    destination: "",
    startDate: "",
    endDate: "",
    travelers: 1,
    budget: "",
  });

  const [travelPlan, setTravelPlan] = useState([]); // Chat-GPTからのプランデータを格納
  const [chatMessages, setChatMessages] = useState([]);
  const [userMessage, setUserMessage] = useState("");

  // Chat-GPTからの応答をバックエンド経由で取得
  const sendTextToBackend = async () => {
    if (userMessage.trim() === "") return;

    // ユーザーのメッセージを追加
    setChatMessages([...chatMessages, { sender: "user", text: userMessage }]);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: userMessage }),
      });

      const data = await response.json();
      console.log(data); // ここでバックエンドの応答を確認

      if (response.ok) {
        // Chat-GPTの応答をチャットに追加
        setChatMessages([
          ...chatMessages,
          { sender: "user", text: userMessage },
          { sender: "bot", text: data.response },
        ]);
        setTravelPlan(data.plan || []); // 旅行プランデータがあれば更新
      } else {
        console.error("Error:", data.error);
      }
    } catch (error) {
      console.error("Error:", error);
    }

    // メッセージ入力をリセット
    setUserMessage("");
  };

  return (
    <div className={styles.travelPlanner}>
      <div className={styles.mainSection}>
        <h1>旅行プランニングサービス</h1>

        <div className={styles.activitySection}>
          <h2>旅行プラン</h2>
          {travelPlan.length === 0 ? (
            <p>旅行プランはまだありません。</p>
          ) : (
            travelPlan.map((day, index) => (
              <div key={index} className={styles.dayPlan}>
                <h3>{day.day}</h3>
                {day.activities.map((activity, idx) => (
                  <div key={idx} className={styles.activityItem}>
                    <span>{activity.time}</span>
                    <span>{activity.description}</span>
                    <span>¥{activity.cost}</span>
                  </div>
                ))}
              </div>
            ))
          )}
        </div>
      </div>

      <div className={styles.chatSection}>
        <h2>Chat-GPTとやりとり</h2>
        <div className={styles.chatBox}>
          {chatMessages.map((msg, index) => (
            <div
              key={index}
              className={`${styles.chatMessage} ${
                msg.sender === "user"
                  ? styles.userMessage
                  : styles.botMessage
              }`}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div className={styles.chatInput}>
          <input
            type="text"
            placeholder="質問や要望を入力"
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
          />
          <button onClick={sendTextToBackend}>送信</button>
        </div>
      </div>
    </div>
  );
};

export default Itineraries;
