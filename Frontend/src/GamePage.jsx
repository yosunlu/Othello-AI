import React, { useEffect, useRef, useState } from "react";
import Logo from "./Logo";
import styles from "./GamePage.module.css";
import OthelloBoard from "./OthelloBoard";
import { useCallback } from "react";

function GamePage() {
  const canvasRef = useRef(null);
  const [started, setStarted] = useState(0); // started is the variable, 0 is what it's initialized w/
  const [ws, setWs] = useState(null);
  const [userId, setUserId] = useState(localStorage.getItem("userid"));
  const [guestId, setGuestId] = useState(localStorage.getItem("guestid"));
  const [whiteCount, setWhiteCount] = useState(2);
  const [blackCount, setBlackCount] = useState(2);

  // Callback function for that will be called in OthelloBoard.js
  const countChangeHandler = useCallback((white, black) => {
    setWhiteCount(white);
    setBlackCount(black);
  }, []);

  const handleConnectClick = () => {
    let gameId;
    if (!userId) {
      if (!guestId) {
        setGuestId(crypto.randomUUID());
        localStorage.setItem("guestid", guestId);
      } else {
        gameId = guestId;
      }
    } else {
      gameId = userId;
    }

    setStarted(1);

    const newWs = new WebSocket(
      "ws://localhost:8000/othelloml_api/ws/pvp-session/" + gameId
    );
    setWs(newWs);

    newWs.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      console.log(msg);
    };

    newWs.onopen = (event) => {
      newWs.send("d");
    };

    newWs.onclose = (event) => {
      alert("Connection lost! This might be intentional.");
    };

    newWs.onerror = (event) => {
      alert("Error occurred!");
    };
  };

  return (
    <div>
      <div className="container py-5">
        <div className={styles.header}>
          <Logo alt="Logo" className={styles.logo} />
          <h1 style={{ fontSize: "60px" }}>Othello ML</h1>
        </div>
        <div className={styles.main}>
          <div className={styles.nav}>
            <a href="#" id={styles.home}>
              Home
            </a>
            <a href="#" className={styles.button} id={styles.newGameBtn}>
              Game
            </a>
            <a href="#">Rules</a>
            <a href="#">About</a>
            <input type="text" placeholder="search player" id={styles.search} />
          </div>
          <div className={styles.game}>
            <div className="text-center ms-3">
              <OthelloBoard
                started={started}
                onDataChange={countChangeHandler}
                whiteCount={whiteCount}
                blackCount={blackCount}
              />
            </div>
            <div className={styles.gameText}>
              <div>
                <div className={styles.count}>
                  <h2 id={styles.numWhite}>White: {whiteCount}</h2>
                  <h2 id={styles.numBlack}>Black: {blackCount}</h2>
                </div>
              </div>
              <div>
                <button id={styles.connectBtn} onClick={handleConnectClick}>
                  Connect
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GamePage;
